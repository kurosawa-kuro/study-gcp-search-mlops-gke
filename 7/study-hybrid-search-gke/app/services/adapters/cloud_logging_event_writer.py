"""Structured event-log adapter for search / impression / action events.

Phase 7 の本線では search-api on GKE から構造化ログを出し、後段の sink /
Pub/Sub / BigQuery curated job で `search_events` / `search_impressions` /
`user_actions` に落とし込む。ここではアプリ contract を先に固定するため、
logger へ JSON payload を best-effort で流す。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from app.domain.event import ActionType
from app.services.protocols.event_writer import EventWriter
from ml.common.logging import get_logger

logger = get_logger("app.adapters.cloud_logging_event_writer")


class CloudLoggingEventWriter(EventWriter):
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
        self._emit(
            {
                "event_name": "search_event",
                "search_id": search_id,
                "user_id": user_id,
                "session_id": session_id,
                "query": query,
                "filters_json": self._parse_json(filters_json),
                "app_version": app_version,
                "model_version": model_version,
            }
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
        self._emit(
            {
                "event_name": "search_impression",
                "search_id": search_id,
                "property_id": property_id,
                "rank": rank,
                "lexical_rank_orig": lexical_rank_orig,
                "semantic_rank_orig": semantic_rank_orig,
                "lexical_score": lexical_score,
                "vector_score": vector_score,
                "rrf_score": rrf_score,
                "rerank_score": rerank_score,
            }
        )

    def emit_user_action(
        self,
        *,
        search_id: str,
        property_id: str,
        action_type: ActionType,
        action_value: float | None = None,
    ) -> None:
        self._emit(
            {
                "event_name": "user_action",
                "search_id": search_id,
                "property_id": property_id,
                "action_type": action_type,
                "action_value": action_value,
            }
        )

    def _emit(self, payload: dict[str, object]) -> None:
        body = {
            **payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "schema_version": 1,
        }
        logger.info(json.dumps(body, ensure_ascii=False, sort_keys=True))

    def _parse_json(self, raw: str) -> object:
        try:
            return json.loads(raw)
        except Exception:
            return raw
