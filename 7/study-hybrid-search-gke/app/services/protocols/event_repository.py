from __future__ import annotations

from datetime import datetime
from typing import Protocol

from app.domain.event import Impression, SearchEvent, UserAction


class EventRepository(Protocol):
    def read_search_events(self, *, since: datetime | None = None) -> list[SearchEvent]: ...

    def read_impressions(
        self,
        *,
        search_id: str | None = None,
        since: datetime | None = None,
    ) -> list[Impression]: ...

    def read_user_actions(
        self,
        *,
        search_id: str | None = None,
        action_type: str | None = None,
        since: datetime | None = None,
    ) -> list[UserAction]: ...
