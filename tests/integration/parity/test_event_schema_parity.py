"""Lock-step contract for the Event schema (Wave 2, 2026-05-06).

`ml/labeling/policy.py` is the **canonical Python source** for the 8-種
``action_type`` enum and weight table. This test pins the lock-step
between 6 canonical 場所:

1. ``ACTION_WEIGHTS_APP_EMIT`` (5 種) ↔ ``app/domain/event.py::ActionType``
   ↔ ``app/schemas/search.py::FeedbackRequest.action`` Literal
2. ``ACTION_WEIGHTS_APP_EMIT`` (5 種) ↔ ``infra/terraform/modules/data/main.tf::user_actions.action_type`` description
3. ``ACTION_WEIGHTS_SYNTHETIC`` (3 種) ↔ ``definitions/labeling/synthetic_actions.yaml`` (action_type / weight / label_source)
4. Combined ``ACTION_WEIGHTS`` (8 種、duplicate-free, all ``int``)
5. ``bounce`` weight == ``-1``、``no_action`` 概念 == ``NO_ACTION_WEIGHT == 0``
6. Terraform ``evaluation_metrics`` テーブル宣言 + canonical metric_name 列挙

A drift here means LightGBM LambdaRank training receives a different
``relevance_label`` set than the app emits, breaking the continuous
improvement cycle silently. canonical 死守ライン (CLAUDE.md 非負制約).
"""

from __future__ import annotations

import re
from typing import get_args

import yaml

from app.domain.event import ActionType
from app.schemas.search import FeedbackRequest
from ml.labeling.policy import (
    ACTION_WEIGHTS,
    ACTION_WEIGHTS_APP_EMIT,
    ACTION_WEIGHTS_SYNTHETIC,
    LABEL_SOURCE_SYNTHETIC_PREFIX,
    NO_ACTION_WEIGHT,
)
from tests.integration.parity.parity_invariant import (
    REPO_ROOT,
    extract_terraform_block,
    read_text,
)

_DATA_TF = REPO_ROOT / "infra" / "terraform" / "modules" / "data" / "main.tf"
_SYNTHETIC_YAML = REPO_ROOT / "definitions" / "labeling" / "synthetic_actions.yaml"


# ---------------------------------------------------------------------------
# 1) ACTION_WEIGHTS_APP_EMIT ↔ Pydantic / domain Literal
# ---------------------------------------------------------------------------


def test_app_emit_keys_match_domain_action_type() -> None:
    """``ACTION_WEIGHTS_APP_EMIT`` keys == ``app/domain/event.py::ActionType`` Literal."""
    domain_values = set(get_args(ActionType))
    assert set(ACTION_WEIGHTS_APP_EMIT.keys()) == domain_values, (
        f"app emit drift: policy={set(ACTION_WEIGHTS_APP_EMIT.keys())} "
        f"vs domain ActionType={domain_values}"
    )


def test_app_emit_keys_match_pydantic_feedback_request() -> None:
    """``ACTION_WEIGHTS_APP_EMIT`` keys == ``FeedbackRequest.action`` Literal."""
    field_annotation = FeedbackRequest.model_fields["action"].annotation
    pydantic_values = set(get_args(field_annotation))
    assert set(ACTION_WEIGHTS_APP_EMIT.keys()) == pydantic_values, (
        f"Pydantic FeedbackRequest.action drift: policy={set(ACTION_WEIGHTS_APP_EMIT.keys())} "
        f"vs Pydantic Literal={pydantic_values}"
    )


# ---------------------------------------------------------------------------
# 2) ACTION_WEIGHTS_APP_EMIT ↔ Terraform user_actions.action_type description
# ---------------------------------------------------------------------------


def test_app_emit_keys_match_terraform_user_actions_description() -> None:
    """user_actions テーブルの ``action_type`` description が 5 種を網羅していること。

    description は人間可読な ``click | detail_view | favorite | ...`` 列挙で書いてあり、
    本テストは 5 種すべてが文字列として現れることを assert する (順序と区切りは緩い)。
    """
    body = extract_terraform_block(
        read_text(_DATA_TF),
        resource_type="google_bigquery_table",
        name="user_actions",
    )
    assert body is not None, "user_actions resource missing in main.tf"
    for action in ACTION_WEIGHTS_APP_EMIT:
        assert action in body, f"Terraform user_actions.action_type description missing {action!r}"


def test_terraform_user_actions_description_excludes_synthetic() -> None:
    """user_actions テーブルは app emit 専用、synthetic 3 種を経由しないことを description で明示。"""
    body = extract_terraform_block(
        read_text(_DATA_TF),
        resource_type="google_bigquery_table",
        name="user_actions",
    )
    assert body is not None
    # description must explicitly call out that synthetic 注入 goes through ranking_labels.
    assert "synthetic" in body and "ranking_labels" in body, (
        "user_actions.action_type description must document the synthetic route boundary"
    )


# ---------------------------------------------------------------------------
# 3) ACTION_WEIGHTS_SYNTHETIC ↔ definitions/labeling/synthetic_actions.yaml
# ---------------------------------------------------------------------------


def _load_synthetic_yaml() -> list[dict[str, object]]:
    payload = yaml.safe_load(_SYNTHETIC_YAML.read_text(encoding="utf-8"))
    assert isinstance(payload, dict), "synthetic_actions.yaml must be a top-level mapping"
    entries = payload.get("synthetic_actions")
    assert isinstance(entries, list), "synthetic_actions.yaml::synthetic_actions must be a list"
    for entry in entries:
        assert isinstance(entry, dict), f"non-mapping entry in synthetic_actions: {entry!r}"
    return entries  # type: ignore[return-value]


def test_synthetic_yaml_action_types_match_policy() -> None:
    """YAML synthetic_actions[*].action_type == ACTION_WEIGHTS_SYNTHETIC keys."""
    yaml_actions = {entry["action_type"] for entry in _load_synthetic_yaml()}
    assert yaml_actions == set(ACTION_WEIGHTS_SYNTHETIC.keys()), (
        f"YAML synthetic drift: yaml={yaml_actions} vs policy={set(ACTION_WEIGHTS_SYNTHETIC.keys())}"
    )


def test_synthetic_yaml_weights_match_policy() -> None:
    """YAML synthetic_actions[*].weight == ACTION_WEIGHTS_SYNTHETIC[<action_type>]."""
    for entry in _load_synthetic_yaml():
        action = entry["action_type"]
        assert ACTION_WEIGHTS_SYNTHETIC[action] == entry["weight"], (
            f"weight drift for {action!r}: policy={ACTION_WEIGHTS_SYNTHETIC[action]} "
            f"vs yaml={entry['weight']}"
        )


def test_synthetic_yaml_label_source_format() -> None:
    """YAML label_source uses ``synthetic_<action_type>`` canonical naming."""
    for entry in _load_synthetic_yaml():
        action = entry["action_type"]
        expected = f"{LABEL_SOURCE_SYNTHETIC_PREFIX}{action}"
        assert entry["label_source"] == expected, (
            f"label_source drift for {action!r}: yaml={entry['label_source']!r}, "
            f"expected={expected!r}"
        )


# ---------------------------------------------------------------------------
# 4) Combined ACTION_WEIGHTS contract
# ---------------------------------------------------------------------------


def test_action_weights_is_app_emit_union_synthetic_no_overlap() -> None:
    """ACTION_WEIGHTS = APP_EMIT + SYNTHETIC, no overlapping keys, all int."""
    overlap = set(ACTION_WEIGHTS_APP_EMIT) & set(ACTION_WEIGHTS_SYNTHETIC)
    assert overlap == set(), f"app emit and synthetic share keys: {overlap}"
    assert ACTION_WEIGHTS == {**ACTION_WEIGHTS_APP_EMIT, **ACTION_WEIGHTS_SYNTHETIC}
    assert len(ACTION_WEIGHTS) == 8, f"expected 8 種, got {len(ACTION_WEIGHTS)}"
    assert all(isinstance(v, int) for v in ACTION_WEIGHTS.values())


# ---------------------------------------------------------------------------
# 5) Pinned weight values (CLAUDE.md non-negotiable spec)
# ---------------------------------------------------------------------------


def test_canonical_weight_values_pinned() -> None:
    """canonical 死守ラインの weight をハードコードで固定。

    docs (CLAUDE.md / 01_仕様と設計.md) の数字を変えるときは必ずここも更新する。
    """
    assert ACTION_WEIGHTS == {
        "click": 1,
        "detail_view": 2,
        "favorite": 3,
        "request_button_click": 4,
        "request_complete": 5,
        "inquiry_complete": 7,
        "contract": 10,
        "bounce": -1,
    }
    assert NO_ACTION_WEIGHT == 0


# ---------------------------------------------------------------------------
# 6) Terraform evaluation_metrics declaration
# ---------------------------------------------------------------------------


def test_evaluation_metrics_table_declared() -> None:
    body = extract_terraform_block(
        read_text(_DATA_TF),
        resource_type="google_bigquery_table",
        name="evaluation_metrics",
    )
    assert body is not None, "evaluation_metrics resource missing in main.tf"
    for required_column in (
        "metric_name",
        "metric_value",
        "evaluated_at",
        "passed",
        "threshold",
    ):
        assert re.search(rf'name\s*=\s*"{required_column}"', body), (
            f"evaluation_metrics schema missing column {required_column!r}"
        )
    # metric_name description must enumerate the canonical metric set so
    # downstream Composer DAG monitoring_validation knows the contract.
    for canonical_metric in ("ndcg_at_10", "recall_at_20", "map", "ctr", "cvr"):
        assert canonical_metric in body, (
            f"evaluation_metrics.metric_name description missing {canonical_metric!r}"
        )


# ---------------------------------------------------------------------------
# 7) ranking_labels description references both label_source values
# ---------------------------------------------------------------------------


def test_ranking_labels_description_documents_label_source_canonical() -> None:
    """ranking_labels.label_source description が user_action と synthetic_* を列挙。"""
    body = extract_terraform_block(
        read_text(_DATA_TF),
        resource_type="google_bigquery_table",
        name="ranking_labels",
    )
    assert body is not None
    for required_label in (
        "user_action",
        "synthetic_inquiry_complete",
        "synthetic_contract",
        "synthetic_bounce",
    ):
        assert required_label in body, (
            f"ranking_labels.label_source description missing {required_label!r}"
        )
