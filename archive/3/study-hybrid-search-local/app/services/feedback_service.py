"""``FeedbackService`` — /feedback orchestration.

Thin wrapper around :class:`FeedbackRecorder` that swallows transient
publish failures (telemetry, not transactional). The HTTP handler maps
the boolean to ``accepted`` in the response.
"""

from __future__ import annotations

from app.domain.event import ActionType
from app.services.protocols.event_writer import EventWriter
from app.services.protocols.feedback_recorder import FeedbackRecorder
from ml.common.logging import get_logger

logger = get_logger("app.feedback_service")

LEGACY_ACTIONS = {"click", "favorite"}


class FeedbackService:
    def __init__(self, *, recorder: FeedbackRecorder, event_writer: EventWriter) -> None:
        self._recorder = recorder
        self._event_writer = event_writer

    def record(
        self,
        *,
        request_id: str,
        property_id: str,
        action: ActionType,
        action_value: float | None = None,
    ) -> bool:
        """Returns ``True`` on successful publish, ``False`` on transient failure."""
        try:
            self._event_writer.emit_user_action(
                search_id=request_id,
                property_id=property_id,
                action_type=action,
                action_value=action_value,
            )
            if action in LEGACY_ACTIONS:
                self._recorder.record(
                    request_id=request_id,
                    property_id=property_id,
                    action=action,
                )
        except Exception:
            logger.exception("Feedback publish failed — continuing")
            return False
        return True
