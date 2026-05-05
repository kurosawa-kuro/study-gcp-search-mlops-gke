from __future__ import annotations

from datetime import datetime
from typing import cast

import psycopg

from app.domain.event import ActionType, Impression, SearchEvent, UserAction
from app.services.protocols.event_repository import EventRepository
from ml.common import get_logger


class PostgresEventRepository(EventRepository):
    def __init__(self, *, dsn: str) -> None:
        self._dsn = dsn
        self._logger = get_logger("app.adapters.postgres_event_repository")

    def read_search_events(self, *, since: datetime | None = None) -> list[SearchEvent]:
        sql = """
            SELECT search_id, query, filters_json::text, user_id, session_id, app_version, model_version, timestamp
            FROM search_events
            WHERE (%s IS NULL OR timestamp >= %s)
            ORDER BY timestamp ASC
        """
        rows = self._fetchall(sql, (since, since))
        return [
            SearchEvent(
                search_id=str(row[0]),
                query=str(row[1]),
                filters_json=str(row[2]),
                user_id=_as_optional_str(row[3]),
                session_id=_as_optional_str(row[4]),
                app_version=_as_optional_str(row[5]),
                model_version=_as_optional_str(row[6]),
                timestamp=_as_optional_datetime(row[7]),
            )
            for row in rows
        ]

    def read_impressions(
        self,
        *,
        search_id: str | None = None,
        since: datetime | None = None,
    ) -> list[Impression]:
        sql = """
            SELECT search_id, property_id, rank, lexical_rank_orig, semantic_rank_orig,
                   lexical_score, vector_score, rrf_score, rerank_score, timestamp
            FROM search_impressions
            WHERE (%s IS NULL OR search_id = %s)
              AND (%s IS NULL OR timestamp >= %s)
            ORDER BY timestamp ASC, rank ASC
        """
        rows = self._fetchall(sql, (search_id, search_id, since, since))
        return [_impression_from_row(row) for row in rows]

    def read_impression(self, *, search_id: str, property_id: str) -> Impression | None:
        sql = """
            SELECT search_id, property_id, rank, lexical_rank_orig, semantic_rank_orig,
                   lexical_score, vector_score, rrf_score, rerank_score, timestamp
            FROM search_impressions
            WHERE search_id = %s AND property_id = %s
            LIMIT 1
        """
        rows = self._fetchall(sql, (search_id, property_id))
        if not rows:
            return None
        return _impression_from_row(rows[0])

    def read_user_actions(
        self,
        *,
        search_id: str | None = None,
        action_type: str | None = None,
        since: datetime | None = None,
    ) -> list[UserAction]:
        sql = """
            SELECT search_id, property_id, action_type::text, action_value, timestamp
            FROM user_actions
            WHERE (%s IS NULL OR search_id = %s)
              AND (%s IS NULL OR action_type::text = %s)
              AND (%s IS NULL OR timestamp >= %s)
            ORDER BY timestamp ASC
        """
        rows = self._fetchall(sql, (search_id, search_id, action_type, action_type, since, since))
        return [
            UserAction(
                search_id=str(row[0]),
                property_id=str(row[1]),
                action_type=cast(ActionType, str(row[2])),
                action_value=_as_optional_float(row[3]),
                timestamp=_as_optional_datetime(row[4]),
            )
            for row in rows
        ]

    def _fetchall(self, sql: str, params: tuple[object, ...]) -> list[tuple[object, ...]]:
        try:
            with psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        except Exception:
            self._logger.exception("event repository query failed")
            return []


def _impression_from_row(row: tuple[object, ...]) -> Impression:
    return Impression(
        search_id=str(row[0]),
        property_id=str(row[1]),
        rank=int(cast(int | str, row[2])),
        lexical_rank_orig=_as_optional_int(row[3]),
        semantic_rank_orig=_as_optional_int(row[4]),
        lexical_score=_as_optional_float(row[5]),
        vector_score=_as_optional_float(row[6]),
        rrf_score=_as_optional_float(row[7]),
        rerank_score=_as_optional_float(row[8]),
        timestamp=_as_optional_datetime(row[9]),
    )


def _as_optional_str(value: object) -> str | None:
    return None if value is None else str(value)


def _as_optional_int(value: object) -> int | None:
    if value is None:
        return None
    return int(cast(int | str, value))


def _as_optional_float(value: object) -> float | None:
    if value is None:
        return None
    return float(cast(float | int | str, value))


def _as_optional_datetime(value: object) -> datetime | None:
    return None if value is None else cast(datetime, value)
