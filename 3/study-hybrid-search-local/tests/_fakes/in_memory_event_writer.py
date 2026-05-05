from __future__ import annotations

from dataclasses import dataclass

from app.domain.event import ActionType
from app.services.protocols.event_writer import EventWriter


@dataclass(frozen=True)
class SearchEventCall:
    search_id: str
    query: str
    filters_json: str
    model_version: str | None


@dataclass(frozen=True)
class ImpressionCall:
    search_id: str
    property_id: str
    rank: int


@dataclass(frozen=True)
class UserActionCall:
    search_id: str
    property_id: str
    action_type: ActionType
    action_value: float | None


class InMemoryEventWriter(EventWriter):
    def __init__(self) -> None:
        self.search_events: list[SearchEventCall] = []
        self.impressions: list[ImpressionCall] = []
        self.user_actions: list[UserActionCall] = []

    def emit_search_event(
        self,
        *,
        search_id: str,
        query: str,
        filters_json: str,
        user_id: str | None = None,
        session_id: str | None = None,
        app_version: str | None = None,
        model_version: str | None = None,
    ) -> None:
        self.search_events.append(
            SearchEventCall(
                search_id=search_id,
                query=query,
                filters_json=filters_json,
                model_version=model_version,
            )
        )

    def emit_impression(
        self,
        *,
        search_id: str,
        property_id: str,
        rank: int,
        lexical_rank_orig: int | None,
        semantic_rank_orig: int | None,
        lexical_score: float | None,
        vector_score: float | None,
        rrf_score: float | None,
        rerank_score: float | None,
    ) -> None:
        self.impressions.append(
            ImpressionCall(search_id=search_id, property_id=property_id, rank=rank)
        )

    def emit_user_action(
        self,
        *,
        search_id: str,
        property_id: str,
        action_type: ActionType,
        action_value: float | None = None,
    ) -> None:
        self.user_actions.append(
            UserActionCall(
                search_id=search_id,
                property_id=property_id,
                action_type=action_type,
                action_value=action_value,
            )
        )
