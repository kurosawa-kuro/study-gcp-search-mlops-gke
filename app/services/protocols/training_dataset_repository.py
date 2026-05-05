"""Port: persist / retrieve training-dataset references in GCS.

The training frame itself (LightGBM LambdaRank input) lives as a Parquet
object under ``gs://<pipeline-root>/training_dataset/...``. This Port only
records the URI + row counts so Composer DAG ``retrain_orchestration``
and ``monitoring_validation`` can hand off to Vertex AI Pipelines without
re-querying BigQuery.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from app.domain.training import TrainingDatasetRef


class TrainingDatasetRepository(Protocol):
    def write_training_dataset(self, ref: TrainingDatasetRef) -> None:
        """Record a newly produced training frame (URI + counts)."""
        ...

    def read_training_dataset(self, *, since: datetime | None = None) -> list[TrainingDatasetRef]:
        """Return training frames produced after ``since`` (newest first)."""
        ...

    def latest_training_dataset(self) -> TrainingDatasetRef | None:
        """Most-recently produced frame, or ``None`` when no run exists."""
        ...
