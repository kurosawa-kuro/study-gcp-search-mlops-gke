"""HTTP-level tests for the ``/api/v1/feedback`` handler."""

from __future__ import annotations


def test_feedback_endpoint_records_event(fake_client, fake_feedback_recorder) -> None:
    response = fake_client.post(
        "/api/v1/feedback",
        json={"request_id": "r-1", "property_id": "P-001", "action": "click"},
    )

    assert response.status_code == 200
    assert response.json() == {"accepted": True}
    assert len(fake_feedback_recorder.events) == 1
    event = fake_feedback_recorder.events[0]
    assert event.request_id == "r-1"
    assert event.property_id == "P-001"
    assert event.action == "click"


def test_feedback_endpoint_rejects_invalid_action(fake_client) -> None:
    response = fake_client.post(
        "/api/v1/feedback",
        json={"request_id": "r-1", "property_id": "P-001", "action": "evil"},
    )
    # Pydantic literal contract enforces the canonical action set.
    assert response.status_code == 422


def test_feedback_endpoint_accepts_all_canonical_actions(fake_client) -> None:
    for action in (
        "click",
        "detail_view",
        "favorite",
        "request_button_click",
        "request_complete",
    ):
        response = fake_client.post(
            "/api/v1/feedback",
            json={"request_id": "r-2", "property_id": "P-010", "action": action},
        )
        assert response.status_code == 200, action
        assert response.json() == {"accepted": True}
