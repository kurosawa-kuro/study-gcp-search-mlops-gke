from __future__ import annotations

import json

import psycopg

from app.domain.event import ActionType
from app.services.protocols.event_writer import EventWriter
from ml.common import get_logger


class PostgresEventWriter(EventWriter):
    def __init__(self, *, dsn: str) -> None:
        self._dsn = dsn
        self._logger = get_logger("app.adapters.postgres_event_writer")

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
        sql = """
            INSERT INTO search_events
                (search_id, user_id, session_id, query, filters_json, app_version, model_version)
            VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s)
            ON CONFLICT (search_id) DO NOTHING
        """
        self._execute(
            sql,
            (
                search_id,
                user_id,
                session_id,
                query,
                filters_json,
                app_version,
                model_version,
            ),
            "emit_search_event",
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
        sql = """
            INSERT INTO search_impressions
                (search_id, property_id, rank, lexical_rank_orig, semantic_rank_orig,
                 lexical_score, vector_score, rrf_score, rerank_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (search_id, property_id) DO UPDATE SET
                rank = EXCLUDED.rank,
                lexical_rank_orig = EXCLUDED.lexical_rank_orig,
                semantic_rank_orig = EXCLUDED.semantic_rank_orig,
                lexical_score = EXCLUDED.lexical_score,
                vector_score = EXCLUDED.vector_score,
                rrf_score = EXCLUDED.rrf_score,
                rerank_score = EXCLUDED.rerank_score,
                timestamp = NOW()
        """
        self._execute(
            sql,
            (
                search_id,
                property_id,
                rank,
                lexical_rank_orig,
                semantic_rank_orig,
                lexical_score,
                vector_score,
                rrf_score,
                rerank_score,
            ),
            "emit_impression",
        )

    def emit_user_action(
        self,
        *,
        search_id: str,
        property_id: str,
        action_type: ActionType,
        action_value: float | None = None,
    ) -> None:
        sql = """
            INSERT INTO user_actions (search_id, property_id, action_type, action_value)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (search_id, property_id, action_type) DO UPDATE SET
                action_value = EXCLUDED.action_value,
                timestamp = NOW()
        """
        self._execute(
            sql,
            (search_id, property_id, action_type, action_value),
            "emit_user_action",
        )

    def _execute(self, sql: str, params: tuple[object, ...], op: str) -> None:
        try:
            with psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
                cur.execute(sql, params)
                conn.commit()
        except Exception:
            self._logger.exception("%s failed", op)


def dump_filters_json(filters: dict[str, object]) -> str:
    return json.dumps(filters, ensure_ascii=False, sort_keys=True)
