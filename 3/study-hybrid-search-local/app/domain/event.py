from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

ActionType = Literal[
    "click",
    "detail_view",
    "favorite",
    "request_button_click",
    "request_complete",
]


@dataclass(frozen=True)
class SearchEvent:
    search_id: str
    query: str
    filters_json: str
    user_id: str | None = None
    session_id: str | None = None
    app_version: str | None = None
    model_version: str | None = None
    timestamp: datetime | None = None


@dataclass(frozen=True)
class Impression:
    search_id: str
    property_id: str
    rank: int
    lexical_rank_orig: int | None
    semantic_rank_orig: int | None
    lexical_score: float | None
    vector_score: float | None
    rrf_score: float | None
    rerank_score: float | None
    timestamp: datetime | None = None


@dataclass(frozen=True)
class UserAction:
    search_id: str
    property_id: str
    action_type: ActionType
    action_value: float | None = None
    timestamp: datetime | None = None
