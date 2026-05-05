"""Unit tests for ``FeedbackService``."""

from __future__ import annotations

from app.services.feedback_service import FeedbackService
from tests._fakes import InMemoryEventWriter, InMemoryFeedbackRecorder


def test_record_returns_true_on_success() -> None:
    recorder = InMemoryFeedbackRecorder()
    service = FeedbackService(recorder=recorder)

    accepted = service.record(request_id="r-1", property_id="P-001", action="click")

    assert accepted is True
    assert len(recorder.events) == 1
    event = recorder.events[0]
    assert event.request_id == "r-1"
    assert event.property_id == "P-001"
    assert event.action == "click"


def test_record_returns_false_on_publish_failure() -> None:
    recorder = InMemoryFeedbackRecorder(fail=True)
    service = FeedbackService(recorder=recorder)

    accepted = service.record(request_id="r-2", property_id="P-002", action="favorite")

    assert accepted is False


def test_record_emits_new_user_action_contract() -> None:
    recorder = InMemoryFeedbackRecorder()
    event_writer = InMemoryEventWriter()
    service = FeedbackService(recorder=recorder, event_writer=event_writer)

    accepted = service.record(
        request_id="r-3",
        property_id="P-003",
        action="request_complete",
    )

    assert accepted is True
    assert len(event_writer.user_actions) == 1
    assert event_writer.user_actions[0].action_type == "request_complete"
    assert recorder.events == []
