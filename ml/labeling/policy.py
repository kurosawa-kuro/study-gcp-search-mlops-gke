"""Canonical Python source for the action_type enum + relevance weights.

Wave 2 (2026-05-06) で 6 canonical 場所 (Pydantic / Terraform / labeling YAML /
labeling SQL / EventWriter Port / `ranking_labels` 書き込み) を 1 本に揃える
ための **Python 側の正本**。docs/architecture/01_仕様と設計.md §1.1 と
CLAUDE.md 非負制約 (Event schema 共通契約) に対応。

経路境界:

- **アプリ emit 5 種** (`ACTION_WEIGHTS_APP_EMIT`): UI / Pydantic
  ``FeedbackRequest.action`` / ``app/domain/event.py::ActionType`` Literal /
  ``EventWriter.emit_user_action`` 経由で BigQuery ``user_actions`` テーブルへ。
- **synthetic 注入 3 種** (`ACTION_WEIGHTS_SYNTHETIC`): アプリから取得不可。
  labeling SQL が ``definitions/labeling/synthetic_actions.yaml`` の trigger /
  probability に従って ``ranking_labels.label_source='synthetic_<type>'``
  形式で擬似正解データとして直接 INSERT。``user_actions`` テーブルや
  EventWriter Port は通らない。
- **`long_stay`** は ``action_type`` enum 値ではなく、``user_actions.action_value``
  修飾子の概念 (``detail_view`` の dwell time として将来格納する予約)。enum 8 種
  にはカウントしない。

LightGBM LambdaRank の学習データ正本は ``ranking_labels`` テーブルの
``relevance_label`` カラム (= ここの weight 値が直接書き込まれる)。
"""

from __future__ import annotations

from collections.abc import Iterable

# アプリ emit 5 種 — Pydantic / EventWriter Port が同期する。
ACTION_WEIGHTS_APP_EMIT: dict[str, int] = {
    "click": 1,
    "detail_view": 2,
    "favorite": 3,
    "request_button_click": 4,
    "request_complete": 5,
}

# synthetic 注入専用 3 種 — labeling SQL が ranking_labels に直接書く。
# ``bounce`` weight は -1 で固定 (LightGBM LambdaRank の負例として明示)。
ACTION_WEIGHTS_SYNTHETIC: dict[str, int] = {
    "inquiry_complete": 7,
    "contract": 10,
    "bounce": -1,
}

# action_type enum 8 種 (BigQuery `user_actions.action_type` enum の論理上のスコープ +
# synthetic 注入経路の合算)。LightGBM 学習に届く relevance label の weight 計算用。
ACTION_WEIGHTS: dict[str, int] = {**ACTION_WEIGHTS_APP_EMIT, **ACTION_WEIGHTS_SYNTHETIC}

# 表示はあったが action が無かった impression の weight。
NO_ACTION_WEIGHT: int = 0

# label_source カラム (ranking_labels.label_source) に書く文字列値の canonical。
LABEL_SOURCE_USER_ACTION: str = "user_action"
LABEL_SOURCE_NO_ACTION: str = "no_action"
LABEL_SOURCE_SYNTHETIC_PREFIX: str = "synthetic_"


def synthetic_label_source(action_type: str) -> str:
    """Return the ``ranking_labels.label_source`` value for a synthetic action.

    Example: ``synthetic_label_source("contract") -> "synthetic_contract"``.
    Caller is responsible for passing one of the keys in
    :data:`ACTION_WEIGHTS_SYNTHETIC` (no validation done here).
    """
    return f"{LABEL_SOURCE_SYNTHETIC_PREFIX}{action_type}"


def compute_label(
    *,
    actions_for_property: Iterable[str],
    impression_present: bool,
) -> tuple[int, str]:
    """Pick the strongest action's weight as the relevance label.

    Treats unknown actions as weight 0 so a future enum extension that
    misses :data:`ACTION_WEIGHTS` does not silently inflate scores.
    Selection is stable for ties (``max`` keeps the first occurrence).
    """
    actions = list(actions_for_property)
    if not impression_present:
        return (NO_ACTION_WEIGHT, "no_impression")
    if not actions:
        return (NO_ACTION_WEIGHT, LABEL_SOURCE_NO_ACTION)
    strongest_action = max(actions, key=lambda action: ACTION_WEIGHTS.get(action, 0))
    return (ACTION_WEIGHTS.get(strongest_action, 0), strongest_action)
