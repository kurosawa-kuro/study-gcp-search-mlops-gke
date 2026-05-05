from __future__ import annotations

from datetime import datetime
from typing import Protocol

from app.domain.labeling import RankingLabel


class LabelRepository(Protocol):
    def write_ranking_labels(self, labels: list[RankingLabel]) -> None: ...

    def read_ranking_labels(self, *, since: datetime | None = None) -> list[RankingLabel]: ...
