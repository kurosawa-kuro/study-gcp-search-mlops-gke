"""``/ops/admin/mlops`` — operator dashboard for the continuous-improvement cycle.

Aggregates a snapshot of:

- event ingestion volumes (`search_events` / `search_impressions` /
  `user_actions` / `ranking_labels`) over the last ``window_days``
- the most-recent training-dataset reference (Parquet URI in GCS)
- the latest evaluation metric per canonical ``metric_name``
  (``ndcg_at_10`` / ``recall_at_20`` / ``map`` / ``ctr`` / ``cvr``)
  + deployment-gate verdicts
- current ``production`` model artifact paths (encoder / reranker)

Mounted under ``/ops`` in ``app/main.py``, so the public path is
``/ops/admin/mlops``. IAP-gated like the rest of ``/ops/*``.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_container
from app.composition_root import Container
from app.schemas.admin_mlops import (
    AdminMlopsResponse,
    EventCounts,
    MetricSnapshot,
    TrainingDatasetSnapshot,
)

router = APIRouter(prefix="/admin")

_CANONICAL_METRIC_NAMES: tuple[str, ...] = (
    "ndcg_at_10",
    "recall_at_20",
    "map",
    "ctr",
    "cvr",
)


@router.get("/mlops", response_model=AdminMlopsResponse)
def admin_mlops(
    container: Annotated[Container, Depends(get_container)],
    window_days: int = Query(7, ge=1, le=365, description="Look-back window in days"),
) -> AdminMlopsResponse:
    """Best-effort continuous-improvement snapshot.

    Each repository call is wrapped so a missing backend (Noop) returns
    zeros / empty lists instead of bubbling errors — the page must remain
    available even when only a subset of the cycle is wired.
    """
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=window_days)

    counts = _collect_event_counts(container, since=since)
    latest_dataset = _collect_latest_dataset(container)
    latest_metrics = _collect_latest_metrics(container)
    return AdminMlopsResponse(
        generated_at=now,
        window_days=window_days,
        event_counts=counts,
        latest_training_dataset=latest_dataset,
        latest_metrics=latest_metrics,
        current_model_path=container.model_path,
        current_encoder_model_path=container.encoder_model_path,
    )


def _collect_event_counts(container: Container, *, since: datetime) -> EventCounts:
    """Count rows in each event table since the cutoff (Noop-safe)."""
    repository = container.event_repository
    label_repo = container.label_repository
    try:
        search_events = len(repository.read_search_events(since=since))
    except Exception:
        search_events = 0
    try:
        impressions = len(repository.read_impressions(since=since))
    except Exception:
        impressions = 0
    try:
        user_actions = len(repository.read_user_actions(since=since))
    except Exception:
        user_actions = 0
    try:
        labels = len(label_repo.read_ranking_labels(since=since))
    except Exception:
        labels = 0
    return EventCounts(
        search_events=search_events,
        search_impressions=impressions,
        user_actions=user_actions,
        ranking_labels=labels,
    )


def _collect_latest_dataset(container: Container) -> TrainingDatasetSnapshot | None:
    try:
        ref = container.training_dataset_repository.latest_training_dataset()
    except Exception:
        return None
    if ref is None:
        return None
    return TrainingDatasetSnapshot(
        uri=ref.uri,
        rows=ref.rows,
        created_at=ref.created_at,
        dataset_version=ref.dataset_version,
    )


def _collect_latest_metrics(container: Container) -> list[MetricSnapshot]:
    try:
        latest = container.metrics_repository.latest_metrics(
            metric_names=list(_CANONICAL_METRIC_NAMES),
        )
    except Exception:
        return []
    return [
        MetricSnapshot(
            metric_name=metric.metric_name,
            metric_value=metric.metric_value,
            threshold=metric.threshold,
            passed=metric.passed,
            evaluated_at=metric.evaluated_at,
            run_id=metric.run_id,
            dataset_version=metric.dataset_version,
        )
        for metric in latest.values()
    ]
