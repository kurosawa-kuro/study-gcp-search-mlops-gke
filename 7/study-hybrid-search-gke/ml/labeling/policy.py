from __future__ import annotations

from collections.abc import Iterable

ACTION_WEIGHTS: dict[str, int] = {
    "click": 1,
    "detail_view": 2,
    "favorite": 3,
    "request_button_click": 4,
    "request_complete": 5,
}


def compute_label(
    *,
    actions_for_property: Iterable[str],
    impression_present: bool,
) -> tuple[int, str]:
    actions = list(actions_for_property)
    if not impression_present:
        return (0, "no_impression")
    if not actions:
        return (0, "no_action")
    strongest_action = max(actions, key=lambda action: ACTION_WEIGHTS.get(action, 0))
    return (ACTION_WEIGHTS.get(strongest_action, 0), strongest_action)
