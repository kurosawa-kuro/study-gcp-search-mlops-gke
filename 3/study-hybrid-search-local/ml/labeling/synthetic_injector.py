from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import yaml

from app.domain.labeling import RankingLabel


@dataclass(frozen=True)
class SyntheticRule:
    name: str
    trigger: str
    probability: float
    label_source: str
    relevance_label: float | None = None
    relevance_label_delta: float | None = None


def load_rules(path: Path) -> list[SyntheticRule]:
    payload = yaml.safe_load(path.read_text()) or {}
    block = payload.get("synthetic_injection", {})
    rules: list[SyntheticRule] = []
    for name, config in block.items():
        rules.append(
            SyntheticRule(
                name=name,
                trigger=str(config["trigger"]),
                probability=float(config["probability"]),
                label_source=str(config["label_source"]),
                relevance_label=(
                    None
                    if config.get("relevance_label") is None
                    else float(config["relevance_label"])
                ),
                relevance_label_delta=(
                    None
                    if config.get("relevance_label_delta") is None
                    else float(config["relevance_label_delta"])
                ),
            )
        )
    return rules


def inject_synthetic_labels(
    *,
    base_labels: dict[tuple[str, str], RankingLabel],
    actions_by_key: dict[tuple[str, str], list[str]],
    fixture_path: Path,
) -> list[RankingLabel]:
    rules = load_rules(fixture_path)
    injected: list[RankingLabel] = []
    for key, base in base_labels.items():
        actions = actions_by_key.get(key, [])
        best_label: RankingLabel | None = None
        for rule in rules:
            if not _trigger_matches(rule.trigger, actions):
                continue
            if not _deterministic_hit(key=key, rule=rule):
                continue
            next_label = _build_label(base=base, rule=rule)
            if next_label is None:
                continue
            if best_label is None or next_label.relevance_label > best_label.relevance_label:
                best_label = next_label
        if best_label is not None:
            injected.append(best_label)
    return injected


def _build_label(*, base: RankingLabel, rule: SyntheticRule) -> RankingLabel | None:
    if rule.relevance_label is not None:
        relevance = rule.relevance_label
    elif rule.relevance_label_delta is not None:
        relevance = base.relevance_label + rule.relevance_label_delta
    else:
        return None
    return RankingLabel(
        search_id=base.search_id,
        property_id=base.property_id,
        relevance_label=relevance,
        label_source=rule.label_source,
    )


def _trigger_matches(trigger: str, actions: list[str]) -> bool:
    action_set = set(actions)
    if trigger == "actions_contains_request_complete":
        return "request_complete" in action_set
    if trigger == "actions_contains_request_complete_and_favorite":
        return {"request_complete", "favorite"}.issubset(action_set)
    if trigger == "actions_only_click":
        return action_set == {"click"}
    if trigger == "actions_contains_detail_view":
        return "detail_view" in action_set
    return False


def _deterministic_hit(*, key: tuple[str, str], rule: SyntheticRule) -> bool:
    seed = f"{rule.name}:{key[0]}:{key[1]}".encode()
    digest = hashlib.sha256(seed).hexdigest()
    threshold = int(rule.probability * 10_000)
    value = int(digest[:8], 16) % 10_000
    return value < threshold
