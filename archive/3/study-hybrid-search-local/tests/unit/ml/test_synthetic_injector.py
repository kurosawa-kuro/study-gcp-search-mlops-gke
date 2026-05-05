from __future__ import annotations

from pathlib import Path

from app.domain.labeling import RankingLabel
from ml.labeling.synthetic_injector import inject_synthetic_labels

FIXTURE = (
    Path(__file__).resolve().parents[3] / "definitions" / "labeling" / "synthetic_actions.yaml"
)


def test_synthetic_injector_is_deterministic() -> None:
    base_labels = {
        ("req-1", "prop-1"): RankingLabel(
            search_id="req-1",
            property_id="prop-1",
            relevance_label=0.0,
            label_source="no_action",
        )
    }
    actions_by_key = {("req-1", "prop-1"): ["click"]}

    left = inject_synthetic_labels(
        base_labels=base_labels,
        actions_by_key=actions_by_key,
        fixture_path=FIXTURE,
    )
    right = inject_synthetic_labels(
        base_labels=base_labels,
        actions_by_key=actions_by_key,
        fixture_path=FIXTURE,
    )

    assert left == right


def test_synthetic_injector_can_add_delta_label() -> None:
    base_labels = {
        ("req-2", "prop-2"): RankingLabel(
            search_id="req-2",
            property_id="prop-2",
            relevance_label=2.0,
            label_source="detail_view",
        )
    }
    actions_by_key = {("req-2", "prop-2"): ["detail_view"]}

    injected = inject_synthetic_labels(
        base_labels=base_labels,
        actions_by_key=actions_by_key,
        fixture_path=FIXTURE,
    )

    assert all(label.search_id == "req-2" for label in injected)
