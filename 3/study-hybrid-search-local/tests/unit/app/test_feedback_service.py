from __future__ import annotations

from app.services.feedback_service import FeedbackService
from tests._fakes import InMemoryEventWriter, InMemoryFeedbackRecorder


def test_feedback_service_writes_new_event_and_legacy_feedback_for_click() -> None:
    recorder = InMemoryFeedbackRecorder()
    event_writer = InMemoryEventWriter()
    service = FeedbackService(recorder=recorder, event_writer=event_writer)

    accepted = service.record(
        request_id="req-1",
        property_id="prop-1",
        action="click",
    )

    assert accepted is True
    assert len(event_writer.user_actions) == 1
    assert event_writer.user_actions[0].action_type == "click"
    assert len(recorder.events) == 1
    assert recorder.events[0].action == "click"


def test_feedback_service_skips_legacy_feedback_for_detail_view() -> None:
    recorder = InMemoryFeedbackRecorder()
    event_writer = InMemoryEventWriter()
    service = FeedbackService(recorder=recorder, event_writer=event_writer)

    accepted = service.record(
        request_id="req-2",
        property_id="prop-2",
        action="detail_view",
    )

    assert accepted is True
    assert len(event_writer.user_actions) == 1
    assert recorder.events == []
