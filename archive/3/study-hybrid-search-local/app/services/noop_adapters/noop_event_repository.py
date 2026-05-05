from __future__ import annotations

from datetime import datetime

from app.domain.event import Impression, SearchEvent, UserAction
from app.services.protocols.event_repository import EventRepository


class NoopEventRepository(EventRepository):
    def read_search_events(self, *, since: datetime | None = None) -> list[SearchEvent]:
        return []

    def read_impressions(
        self,
        *,
        search_id: str | None = None,
        since: datetime | None = None,
    ) -> list[Impression]:
        return []

    def read_impression(self, *, search_id: str, property_id: str) -> Impression | None:
        return None

    def read_user_actions(
        self,
        *,
        search_id: str | None = None,
        action_type: str | None = None,
        since: datetime | None = None,
    ) -> list[UserAction]:
        return []
