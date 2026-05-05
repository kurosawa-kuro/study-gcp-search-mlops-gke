from __future__ import annotations

from app.domain.event import ActionType, Impression, SearchEvent, UserAction
from app.services.protocols.event_writer import EventWriter


class InMemoryEventWriter(EventWriter):
    def __init__(self, *, fail: bool = False) -> None:
        self._fail = fail
        self.search_events: list[SearchEvent] = []
        self.impressions: list[Impression] = []
        self.user_actions: list[UserAction] = []

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
        self._raise_if_needed()
        self.search_events.append(
            SearchEvent(
                search_id=search_id,
                query=query,
                filters_json=filters_json,
                user_id=user_id,
                session_id=session_id,
                app_version=app_version,
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
        self._raise_if_needed()
        self.impressions.append(
            Impression(
                search_id=search_id,
                property_id=property_id,
                rank=rank,
                lexical_rank_orig=lexical_rank_orig,
                semantic_rank_orig=semantic_rank_orig,
                lexical_score=lexical_score,
                vector_score=vector_score,
                rrf_score=rrf_score,
                rerank_score=rerank_score,
            )
        )

    def emit_user_action(
        self,
        *,
        search_id: str,
        property_id: str,
        action_type: ActionType,
        action_value: float | None = None,
    ) -> None:
        self._raise_if_needed()
        self.user_actions.append(
            UserAction(
                search_id=search_id,
                property_id=property_id,
                action_type=action_type,
                action_value=action_value,
            )
        )

    def _raise_if_needed(self) -> None:
        if self._fail:
            raise RuntimeError("InMemoryEventWriter configured to raise")
