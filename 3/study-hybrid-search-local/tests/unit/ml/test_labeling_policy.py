from __future__ import annotations

from ml.labeling.policy import compute_label


def test_compute_label_returns_no_action_when_impression_without_actions() -> None:
    relevance, source = compute_label(actions_for_property=[], impression_present=True)
    assert relevance == 0.0
    assert source == "no_action"


def test_compute_label_picks_strongest_action() -> None:
    relevance, source = compute_label(
        actions_for_property=["click", "favorite", "detail_view"],
        impression_present=True,
    )
    assert relevance == 3.0
    assert source == "favorite"


def test_compute_label_handles_bounce() -> None:
    relevance, source = compute_label(
        actions_for_property=["click", "bounce"],
        impression_present=True,
    )
    assert relevance == -1.0
    assert source == "bounce"
