from __future__ import annotations

from app.domain.event import ActionType
from app.services.protocols.event_writer import EventWriter


class NoopEventWriter(EventWriter):
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
        return None

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
        return None

    def emit_user_action(
        self,
        *,
        search_id: str,
        property_id: str,
        action_type: ActionType,
        action_value: float | None = None,
    ) -> None:
        return None
