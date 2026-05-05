from __future__ import annotations

from datetime import datetime

from app.domain.labeling import RankingLabel
from app.services.protocols.label_repository import LabelRepository


class NoopLabelRepository(LabelRepository):
    def write_ranking_labels(self, labels: list[RankingLabel]) -> None:
        return None

    def read_ranking_labels(self, *, since: datetime | None = None) -> list[RankingLabel]:
        return []
