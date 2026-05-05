from __future__ import annotations

from collections.abc import Iterable

ACTION_WEIGHTS: dict[str, float] = {
    "click": 1.0,
    "detail_view": 2.0,
    "favorite": 3.0,
    "request_button_click": 4.0,
    "request_complete": 5.0,
    "inquiry_complete": 7.0,
    "contract": 10.0,
    "bounce": -1.0,
}


def compute_label(
    *,
    actions_for_property: Iterable[str],
    impression_present: bool,
) -> tuple[float, str]:
    actions = list(actions_for_property)
    if not impression_present:
        return (0.0, "no_impression")
    if not actions:
        return (0.0, "no_action")
    if "bounce" in actions:
        return (-1.0, "bounce")
    strongest_action = max(actions, key=lambda action: ACTION_WEIGHTS.get(action, 0.0))
    return (float(ACTION_WEIGHTS.get(strongest_action, 0.0)), strongest_action)
