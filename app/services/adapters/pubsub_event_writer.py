"""``EventWriter`` adapter — Pub/Sub on canonical 3 topics.

`search-api` から `mlops.{search_events,search_impressions,user_actions}` への
書込み経路を Pub/Sub Subscription (`use_table_schema=true`) 経由で確立する。
CloudLoggingEventWriter は sink 不在で BQ に届かない silent gap があったため、
canonical では本 adapter を使う。

各 emit は 1 publish (timeout 5s)。失敗時は raise (caller が retry / 503 を選ぶ)。

Schema は payload field 名が BQ table column 名と一致する前提
(`use_table_schema=true` + `drop_unknown_fields=true`)。新フィールド追加時は
infra/terraform/modules/data/main.tf の table schema と本 payload の双方を同
PR で更新すること。
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime, timezone

from app.domain.event import ActionType
from app.services.adapters.internal.pubsub_diagnostics import (
    log_publish_failure,
    logger,
    runtime_sa_hint,
)
from app.services.protocols.event_writer import EventWriter


class PubSubEventWriter(EventWriter):
    """Publishes search_event / impression / user_action to 3 Pub/Sub topics."""

    def __init__(
        self,
        *,
        project_id: str,
        search_events_topic: str,
        search_impressions_topic: str,
        user_actions_topic: str,
    ) -> None:
        from google.cloud import pubsub_v1  # type: ignore[attr-defined]

        self._client = pubsub_v1.PublisherClient()
        self._search_events_path = self._client.topic_path(project_id, search_events_topic)
        self._search_impressions_path = self._client.topic_path(
            project_id, search_impressions_topic
        )
        self._user_actions_path = self._client.topic_path(project_id, user_actions_topic)
        logger.info(
            "pubsub.publisher init class=%s search_events=%s search_impressions=%s "
            "user_actions=%s sa_hint=%s",
            type(self).__name__,
            self._search_events_path,
            self._search_impressions_path,
            self._user_actions_path,
            runtime_sa_hint(),
        )

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
        payload = {
            "search_id": search_id,
            "timestamp": _now_iso(),
            "query": query,
            "filters_json": filters_json,
            "user_id": user_id,
            "session_id": session_id,
            "app_version": app_version,
            "model_version": model_version,
            "schema_version": 1,
        }
        self._publish(self._search_events_path, payload, where="emit_search_event")

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
        payload = {
            "search_id": search_id,
            "property_id": property_id,
            "rank": rank,
            "lexical_rank_orig": lexical_rank_orig,
            "semantic_rank_orig": semantic_rank_orig,
            "lexical_score": lexical_score,
            "vector_score": vector_score,
            "rrf_score": rrf_score,
            "rerank_score": rerank_score,
            "timestamp": _now_iso(),
            "schema_version": 1,
        }
        self._publish(self._search_impressions_path, payload, where="emit_impression")

    def emit_user_action(
        self,
        *,
        search_id: str,
        property_id: str,
        action_type: ActionType,
        action_value: float | None = None,
    ) -> None:
        payload = {
            "search_id": search_id,
            "property_id": property_id,
            "action_type": str(action_type),
            "action_value": action_value,
            "timestamp": _now_iso(),
            "schema_version": 1,
        }
        self._publish(self._user_actions_path, payload, where="emit_user_action")

    def _publish(self, topic_path: str, payload: Mapping[str, object], *, where: str) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            self._client.publish(topic_path, data).result(timeout=5)
        except Exception as exc:
            log_publish_failure(
                where=f"PubSubEventWriter.{where}",
                topic_path=topic_path,
                exc=exc,
            )
            raise


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
