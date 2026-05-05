"""Pydantic response schemas for ``/ops/admin/mlops``."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class MetricSnapshot(BaseModel):
    metric_name: str
    metric_value: float
    threshold: float | None = None
    passed: bool | None = None
    evaluated_at: datetime
    run_id: str
    dataset_version: str | None = None


class TrainingDatasetSnapshot(BaseModel):
    uri: str
    rows: int
    created_at: datetime | None = None
    dataset_version: str | None = None


class EventCounts(BaseModel):
    """Best-effort row counts from the most-recent ``window_days`` window."""

    search_events: int = 0
    search_impressions: int = 0
    user_actions: int = 0
    ranking_labels: int = 0


class AdminMlopsResponse(BaseModel):
    """Aggregated snapshot of the continuous-improvement cycle.

    Surfaced at ``/ops/admin/mlops`` for operators to inspect:

    - event ingestion volumes (search_events / search_impressions /
      user_actions / ranking_labels)
    - latest training dataset reference
    - latest evaluation metric per canonical metric_name
    - current ``production`` model alias info
    """

    generated_at: datetime
    window_days: int = Field(ge=1, le=365)
    event_counts: EventCounts
    latest_training_dataset: TrainingDatasetSnapshot | None = None
    latest_metrics: list[MetricSnapshot] = Field(default_factory=list)
    current_model_path: str | None = None
    current_encoder_model_path: str | None = None
