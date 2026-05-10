"""Unit tests for ``PubSubEventWriter``.

Pin the canonical 3-topic emit shape (search-events / search-impressions /
user-actions) so the silent-gap incident (CloudLoggingEventWriter writing to
Cloud Logging without a downstream BQ sink) cannot regress.
"""

from __future__ import annotations

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from app.services.adapters import PubSubEventWriter


def _client_for(project_id: str = "p") -> tuple[MagicMock, MagicMock]:
    fake_client = MagicMock()
    fake_future = MagicMock()
    fake_client.publish.return_value = fake_future

    def topic_path(project: str, topic: str) -> str:
        return f"projects/{project}/topics/{topic}"

    fake_client.topic_path.side_effect = topic_path
    return fake_client, fake_future


def _build(
    fake_client: MagicMock,
) -> PubSubEventWriter:
    with patch("google.cloud.pubsub_v1.PublisherClient", return_value=fake_client):
        return PubSubEventWriter(
            project_id="p",
            search_events_topic="search-events",
            search_impressions_topic="search-impressions",
            user_actions_topic="user-actions",
        )


def test_emit_search_event_publishes_to_search_events_topic() -> None:
    fake_client, fake_future = _client_for()
    writer = _build(fake_client)
    writer.emit_search_event(
        search_id="s1",
        query="赤羽駅",
        filters_json='{"max_rent": 90000}',
        user_id="u1",
        session_id="ses1",
        app_version="1.0",
        model_version="m-2026-05-10",
    )
    topic_path, data = fake_client.publish.call_args.args
    assert topic_path == "projects/p/topics/search-events"
    payload = json.loads(data.decode("utf-8"))
    assert payload["search_id"] == "s1"
    assert payload["query"] == "赤羽駅"
    assert payload["filters_json"] == '{"max_rent": 90000}'
    assert payload["user_id"] == "u1"
    assert payload["app_version"] == "1.0"
    assert payload["model_version"] == "m-2026-05-10"
    assert payload["schema_version"] == 1
    # `timestamp` must be ISO-8601 with timezone offset (BQ TIMESTAMP REQUIRED).
    datetime.fromisoformat(payload["timestamp"])
    fake_future.result.assert_called_once_with(timeout=5)


def test_emit_impression_publishes_to_search_impressions_topic() -> None:
    fake_client, _ = _client_for()
    writer = _build(fake_client)
    writer.emit_impression(
        search_id="s1",
        property_id="p001",
        rank=3,
        lexical_rank_orig=5,
        semantic_rank_orig=2,
        lexical_score=0.81,
        vector_score=0.74,
        rrf_score=0.65,
        rerank_score=0.92,
    )
    topic_path, data = fake_client.publish.call_args.args
    assert topic_path == "projects/p/topics/search-impressions"
    payload = json.loads(data.decode("utf-8"))
    assert payload["search_id"] == "s1"
    assert payload["property_id"] == "p001"
    assert payload["rank"] == 3
    assert payload["lexical_rank_orig"] == 5
    assert payload["rerank_score"] == 0.92
    assert payload["schema_version"] == 1


def test_emit_user_action_publishes_to_user_actions_topic() -> None:
    fake_client, _ = _client_for()
    writer = _build(fake_client)
    writer.emit_user_action(
        search_id="s1",
        property_id="p001",
        action_type="click",
        action_value=1.0,
    )
    topic_path, data = fake_client.publish.call_args.args
    assert topic_path == "projects/p/topics/user-actions"
    payload = json.loads(data.decode("utf-8"))
    assert payload["search_id"] == "s1"
    assert payload["property_id"] == "p001"
    # action_type は str に正規化される (BQ schema = STRING REQUIRED)。
    assert payload["action_type"] == "click"
    assert payload["action_value"] == 1.0
    assert payload["schema_version"] == 1


def test_publish_failure_is_logged_and_reraised() -> None:
    fake_client, _ = _client_for()
    fake_future = MagicMock()
    fake_future.result.side_effect = RuntimeError("permission denied")
    fake_client.publish.return_value = fake_future
    writer = _build(fake_client)
    with pytest.raises(RuntimeError, match="permission denied"):
        writer.emit_user_action(
            search_id="s1",
            property_id="p001",
            action_type="click",
        )


# ---------------------------------------------------------------------------
# build_event_writer selection logic
# ---------------------------------------------------------------------------


def _api_settings(**overrides: object):
    """Build ApiSettings with sensible defaults for selection-logic tests."""
    from app.settings import ApiSettings

    base: dict[str, object] = {
        "project_id": "mlops-test",
        "enable_search": True,
        "enable_rerank": False,
    }
    base.update(overrides)
    return ApiSettings(**base)  # type: ignore[arg-type]


def test_build_event_writer_selects_pubsub_when_topics_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default canonical settings (= 3 topics defined) → PubSubEventWriter."""
    from app.composition_root import ContainerBuilder
    from app.services.adapters import PubSubEventWriter

    fake_client, _ = _client_for(project_id="mlops-test")
    monkeypatch.setattr("google.cloud.pubsub_v1.PublisherClient", lambda: fake_client)
    # Stub the other Pub/Sub publishers + BigQuery client to keep the test
    # isolated from un-related construction logic.
    monkeypatch.setattr("app.container.infra.PubSubRankingLogPublisher", lambda **kw: object())
    monkeypatch.setattr("app.container.infra.PubSubFeedbackRecorder", lambda **kw: object())
    monkeypatch.setattr(ContainerBuilder, "_bigquery", lambda self: MagicMock())

    settings = _api_settings()
    from app.container.infra import InfraBuilder

    writer = InfraBuilder(ContainerBuilder(settings)).build_event_writer()
    assert isinstance(writer, PubSubEventWriter)


def test_build_event_writer_falls_back_to_cloud_logging_when_topic_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty topic name → CloudLoggingEventWriter fallback (bootstrap path)."""
    from app.composition_root import ContainerBuilder
    from app.services.adapters import CloudLoggingEventWriter

    monkeypatch.setattr("app.container.infra.PubSubRankingLogPublisher", lambda **kw: object())
    monkeypatch.setattr("app.container.infra.PubSubFeedbackRecorder", lambda **kw: object())
    monkeypatch.setattr(ContainerBuilder, "_bigquery", lambda self: MagicMock())

    settings = _api_settings(search_events_topic="")  # one topic missing
    from app.container.infra import InfraBuilder

    writer = InfraBuilder(ContainerBuilder(settings)).build_event_writer()
    assert isinstance(writer, CloudLoggingEventWriter)
