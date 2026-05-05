"""Ranker training data + run-metadata store (BigQuery-backed).

Contains the Protocol (:class:`RankerTrainingRepository`) and the BigQuery
implementation. Assembles the LambdaRank training set by joining
``mlops.ranking_labels`` to ``mlops.search_impressions`` and the latest
``feature_mart.property_features_daily`` snapshot. Rows are ordered by
``request_id`` followed by ``rank`` so LightGBM group sizes line up directly.

``save_run`` writes ranker metrics (``ndcg_at_10`` / ``map`` /
``recall_at_20`` / ``best_iteration``) + LambdaRank hyperparameters into
``mlops.training_runs``.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Protocol

import pandas as pd

from ml.common.config import TrainSettings
from ml.common.logging import get_logger

logger = get_logger(__name__)


class RankerTrainingRepository(Protocol):
    def fetch_training_rows(self, *, window_days: int) -> pd.DataFrame:
        """Return a DataFrame sorted contiguously by ``request_id``."""
        ...

    def save_run(
        self,
        *,
        run_id: str,
        started_at: datetime,
        finished_at: datetime,
        model_path: str,
        metrics: dict[str, float],
        hyperparams: dict[str, object],
        git_sha: str | None = None,
        dataset_version: str | None = None,
    ) -> None: ...

    def latest_model_path(self) -> str | None: ...


_TRAINING_SELECT = """
  WITH latest_features AS (
    SELECT
      property_id,
      rent,
      walk_min,
      age_years,
      area_m2,
      ctr,
      fav_rate,
      inquiry_rate
    FROM `{feature_table}`
    WHERE event_date = (SELECT MAX(event_date) FROM `{feature_table}`)
  )
  SELECT
    rl.search_id AS request_id,
    rl.property_id,
    COALESCE(f.rent, r.features.rent) AS rent,
    COALESCE(f.walk_min, r.features.walk_min) AS walk_min,
    COALESCE(f.age_years, r.features.age_years) AS age_years,
    COALESCE(f.area_m2, r.features.area_m2) AS area_m2,
    COALESCE(f.ctr, r.features.ctr) AS ctr,
    COALESCE(f.fav_rate, r.features.fav_rate) AS fav_rate,
    COALESCE(f.inquiry_rate, r.features.inquiry_rate) AS inquiry_rate,
    COALESCE(si.vector_score, r.features.me5_score) AS me5_score,
    COALESCE(CAST(si.lexical_rank_orig AS FLOAT64), r.features.lexical_rank) AS lexical_rank,
    COALESCE(CAST(si.semantic_rank_orig AS FLOAT64), r.features.semantic_rank, 0.0) AS semantic_rank,
    GREATEST(rl.relevance_label, 0) AS label
  FROM `{ranking_labels}` rl
  JOIN `{search_impressions}` si
    ON si.search_id = rl.search_id
   AND si.property_id = rl.property_id
  LEFT JOIN `{ranking_log}` r
    ON r.request_id = rl.search_id
   AND r.property_id = rl.property_id
  LEFT JOIN latest_features f
    ON f.property_id = rl.property_id
  WHERE rl.created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @window_days DAY)
  ORDER BY rl.search_id, si.rank
"""


class BigQueryRankerRepository:
    """BigQuery-backed ranker training repository."""

    def __init__(
        self,
        *,
        project_id: str,
        ranking_log_table: str,
        ranking_labels_table: str,
        search_impressions_table: str,
        feature_table: str,
        training_runs_table: str,
        client: object | None = None,
    ) -> None:
        from google.cloud import bigquery

        self._project_id = project_id
        self._ranking_log_table = ranking_log_table
        self._ranking_labels_table = ranking_labels_table
        self._search_impressions_table = search_impressions_table
        self._feature_table = feature_table
        self._training_runs_table = training_runs_table
        self._client = client or bigquery.Client(project=project_id)

    def fetch_training_rows(self, *, window_days: int) -> pd.DataFrame:
        from google.cloud import bigquery

        query = _TRAINING_SELECT.format(
            ranking_log=self._ranking_log_table,
            ranking_labels=self._ranking_labels_table,
            search_impressions=self._search_impressions_table,
            feature_table=self._feature_table,
        )
        logger.info(
            "Fetching ranker training rows (window=%dd) from %s",
            window_days,
            self._ranking_log_table,
        )
        job = self._client.query(  # type: ignore[attr-defined]
            query,
            job_config=bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("window_days", "INT64", window_days)
                ]
            ),
        )
        df = job.result().to_dataframe(create_bqstorage_client=True)
        logger.info("Fetched %d rows spanning %d request_ids", len(df), df["request_id"].nunique())
        return df

    def save_run(
        self,
        *,
        run_id: str,
        started_at: datetime,
        finished_at: datetime,
        model_path: str,
        metrics: dict[str, float],
        hyperparams: dict[str, object],
        git_sha: str | None = None,
        dataset_version: str | None = None,
    ) -> None:
        self._log_vertex_experiment(run_id=run_id, metrics=metrics, hyperparams=hyperparams)

        row = {
            "run_id": run_id,
            "started_at": started_at.astimezone(timezone.utc).isoformat(),
            "finished_at": finished_at.astimezone(timezone.utc).isoformat(),
            "model_path": model_path,
            "git_sha": git_sha,
            "dataset_version": dataset_version,
            "metrics": {
                k: metrics.get(k) for k in ("best_iteration", "ndcg_at_10", "map", "recall_at_20")
            },
            "hyperparams": {
                k: hyperparams.get(k)
                for k in (
                    "num_leaves",
                    "learning_rate",
                    "feature_fraction",
                    "bagging_fraction",
                    "num_iterations",
                    "early_stopping_rounds",
                    "min_data_in_leaf",
                    "lambdarank_truncation_level",
                )
            },
        }
        errors = self._client.insert_rows_json(self._training_runs_table, [row])  # type: ignore[attr-defined]
        if errors:
            raise RuntimeError(f"BigQuery insert_rows_json failed: {errors}")
        logger.info("Recorded ranker run %s in %s", run_id, self._training_runs_table)

    def _log_vertex_experiment(
        self,
        *,
        run_id: str,
        metrics: dict[str, float],
        hyperparams: dict[str, object],
    ) -> None:
        """Dual-write metrics / params to Vertex AI Experiments.

        Run 3 で `aiplatform.*` 直叩きを `VertexExperimentsTracker` adapter
        (`ml/training/experiments/adapters/vertex_experiments_tracker.py`)
        に外出し。Repository は env→adapter 構築 + try/except のみ担う。
        """
        experiment_name = os.getenv("VERTEX_EXPERIMENT_NAME", "").strip()
        if not experiment_name:
            return
        try:
            # Lazy import: keep the Vertex SDK off the import path of plain
            # repository unit tests (those construct the class with an
            # injected fake BQ client and never reach this branch).
            from ml.training.experiments.adapters.vertex_experiments_tracker import (
                VertexExperimentsTracker,
            )

            with VertexExperimentsTracker(
                project_id=self._project_id,
                experiment_name=experiment_name,
                run_id=run_id,
            ) as tracker:
                tracker.log_params(hyperparams)
                tracker.log_metrics(metrics)
        except Exception:
            logger.exception("Vertex Experiments logging failed for run %s", run_id)

    def latest_model_path(self) -> str | None:
        query = f"""
            SELECT model_path
            FROM `{self._training_runs_table}`
            WHERE finished_at IS NOT NULL
            ORDER BY finished_at DESC
            LIMIT 1
        """
        rows = list(self._client.query(query).result())  # type: ignore[attr-defined]
        return rows[0]["model_path"] if rows else None


def create_rank_repository(settings: TrainSettings) -> RankerTrainingRepository:
    """Build the BQ-backed :class:`RankerTrainingRepository` from settings."""
    project = settings.project_id
    return BigQueryRankerRepository(
        project_id=project,
        ranking_log_table=f"{project}.{settings.bq_dataset_mlops}.ranking_log",
        ranking_labels_table=f"{project}.{settings.bq_dataset_mlops}.ranking_labels",
        search_impressions_table=f"{project}.{settings.bq_dataset_mlops}.search_impressions",
        feature_table=(
            f"{project}.{settings.bq_dataset_feature_mart}.{settings.bq_table_property_features_daily}"
        ),
        training_runs_table=(
            f"{project}.{settings.bq_dataset_mlops}.{settings.bq_table_training_runs}"
        ),
    )
