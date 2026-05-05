from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import cast

from google.cloud import bigquery

from app.domain.training import EvaluationMetric
from app.services.protocols.metrics_repository import MetricsRepository
from ml.common.logging import get_logger


class BigQueryMetricsRepository(MetricsRepository):
    """BigQuery-backed adapter for ``mlops.evaluation_metrics``.

    Schema mirrors ``infra/terraform/modules/data/main.tf::evaluation_metrics``
    (run_id / metric_name / metric_value / threshold / passed / evaluated_at /
    dataset_version / payload). Only the canonical columns are wired here;
    ``payload`` JSON is left to whatever Composer DAG inserts directly.
    """

    def __init__(
        self,
        *,
        client: bigquery.Client,
        evaluation_metrics_table: str,
    ) -> None:
        self._client = client
        self._evaluation_metrics_table = evaluation_metrics_table
        self._logger = get_logger("app.adapters.bigquery_metrics_repository")

    def write_evaluation_metrics(self, metrics: list[EvaluationMetric]) -> None:
        if not metrics:
            return
        rows = [
            {
                "run_id": metric.run_id,
                "dataset_version": metric.dataset_version,
                "metric_name": metric.metric_name,
                "metric_value": float(metric.metric_value),
                "threshold": (float(metric.threshold) if metric.threshold is not None else None),
                "passed": metric.passed,
                "evaluated_at": (metric.evaluated_at or datetime.now(timezone.utc)).isoformat(),
                "payload": None,
            }
            for metric in metrics
        ]
        try:
            errors = self._client.insert_rows_json(
                table=self._evaluation_metrics_table,
                json_rows=rows,
                row_ids=[str(uuid.uuid4()) for _ in rows],
            )
            if errors:
                self._logger.error("evaluation_metrics insert errors: %s", errors)
        except Exception:
            self._logger.exception(
                "write_evaluation_metrics failed for run_id=%s",
                metrics[0].run_id,
            )

    def read_evaluation_metrics(
        self,
        *,
        run_id: str | None = None,
        metric_name: str | None = None,
        since: datetime | None = None,
    ) -> list[EvaluationMetric]:
        clauses: list[str] = []
        params: list[bigquery.ScalarQueryParameter] = []
        if run_id is not None:
            clauses.append("run_id = @run_id")
            params.append(bigquery.ScalarQueryParameter("run_id", "STRING", run_id))
        if metric_name is not None:
            clauses.append("metric_name = @metric_name")
            params.append(bigquery.ScalarQueryParameter("metric_name", "STRING", metric_name))
        if since is not None:
            clauses.append("evaluated_at >= @since")
            params.append(bigquery.ScalarQueryParameter("since", "TIMESTAMP", since))
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"""
            SELECT
              run_id,
              dataset_version,
              metric_name,
              metric_value,
              threshold,
              passed,
              evaluated_at
            FROM `{self._evaluation_metrics_table}`
            {where}
            ORDER BY evaluated_at DESC
        """
        try:
            rows = self._client.query(
                sql,
                job_config=bigquery.QueryJobConfig(query_parameters=params),
            ).result()
        except Exception:
            self._logger.exception("read_evaluation_metrics failed")
            return []
        return [
            EvaluationMetric(
                run_id=str(row["run_id"]),
                metric_name=str(row["metric_name"]),
                metric_value=float(cast(float | int, row["metric_value"] or 0.0)),
                evaluated_at=cast(datetime, row["evaluated_at"]),
                threshold=(
                    float(cast(float | int, row["threshold"]))
                    if row["threshold"] is not None
                    else None
                ),
                passed=cast(bool | None, row["passed"]),
                dataset_version=cast(str | None, row["dataset_version"]),
            )
            for row in rows
        ]

    def latest_metrics(self, *, metric_names: list[str]) -> dict[str, EvaluationMetric]:
        if not metric_names:
            return {}
        sql = f"""
            WITH ranked AS (
              SELECT
                run_id,
                dataset_version,
                metric_name,
                metric_value,
                threshold,
                passed,
                evaluated_at,
                ROW_NUMBER() OVER (PARTITION BY metric_name ORDER BY evaluated_at DESC) AS rn
              FROM `{self._evaluation_metrics_table}`
              WHERE metric_name IN UNNEST(@names)
            )
            SELECT * FROM ranked WHERE rn = 1
        """
        try:
            rows = self._client.query(
                sql,
                job_config=bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ArrayQueryParameter("names", "STRING", metric_names),
                    ],
                ),
            ).result()
        except Exception:
            self._logger.exception("latest_metrics failed")
            return {}
        out: dict[str, EvaluationMetric] = {}
        for row in rows:
            metric = EvaluationMetric(
                run_id=str(row["run_id"]),
                metric_name=str(row["metric_name"]),
                metric_value=float(cast(float | int, row["metric_value"] or 0.0)),
                evaluated_at=cast(datetime, row["evaluated_at"]),
                threshold=(
                    float(cast(float | int, row["threshold"]))
                    if row["threshold"] is not None
                    else None
                ),
                passed=cast(bool | None, row["passed"]),
                dataset_version=cast(str | None, row["dataset_version"]),
            )
            out[metric.metric_name] = metric
        return out
