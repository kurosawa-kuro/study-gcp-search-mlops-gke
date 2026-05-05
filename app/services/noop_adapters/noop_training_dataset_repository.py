"""Noop fallback for :class:`TrainingDatasetRepository`."""

from __future__ import annotations

from datetime import datetime

from app.domain.training import TrainingDatasetRef
from app.services.protocols.training_dataset_repository import TrainingDatasetRepository


class NoopTrainingDatasetRepository(TrainingDatasetRepository):
    """Returns no-ops; used when the GCS bucket is not configured."""

    def write_training_dataset(self, ref: TrainingDatasetRef) -> None:  # noqa: ARG002
        return None

    def read_training_dataset(
        self,
        *,
        since: datetime | None = None,  # noqa: ARG002
    ) -> list[TrainingDatasetRef]:
        return []

    def latest_training_dataset(self) -> TrainingDatasetRef | None:
        return None
