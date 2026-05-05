from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RankingLabel:
    search_id: str
    property_id: str
    relevance_label: float
    label_source: str
    created_at: datetime | None = None
