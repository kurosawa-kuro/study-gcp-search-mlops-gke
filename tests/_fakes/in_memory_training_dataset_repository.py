"""In-memory fake for :class:`TrainingDatasetRepository` (unit tests)."""

from __future__ import annotations

from datetime import datetime

from app.domain.training import TrainingDatasetRef
from app.services.protocols.training_dataset_repository import TrainingDatasetRepository


class InMemoryTrainingDatasetRepository(TrainingDatasetRepository):
    def __init__(self, refs: list[TrainingDatasetRef] | None = None) -> None:
        self._refs: list[TrainingDatasetRef] = list(refs or [])

    def write_training_dataset(self, ref: TrainingDatasetRef) -> None:
        self._refs.append(ref)

    def read_training_dataset(self, *, since: datetime | None = None) -> list[TrainingDatasetRef]:
        records = list(self._refs)
        if since is not None:
            records = [r for r in records if r.created_at and r.created_at >= since]
        records.sort(key=lambda r: r.created_at or datetime.min, reverse=True)
        return records

    def latest_training_dataset(self) -> TrainingDatasetRef | None:
        records = self.read_training_dataset()
        return records[0] if records else None

    @property
    def refs(self) -> list[TrainingDatasetRef]:
        """Test-only accessor."""
        return list(self._refs)
