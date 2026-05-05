from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.domain.labeling import RankingLabel
from app.services.adapters.postgres_event_repository import PostgresEventRepository
from app.services.adapters.postgres_label_repository import PostgresLabelRepository
from ml.common import get_logger
from ml.common.config import TrainSettings
from ml.labeling.policy import compute_label
from ml.labeling.synthetic_injector import inject_synthetic_labels

logger = get_logger("pipeline.labeling_job")


def run(*, dsn: str, fixture_path: Path, since: datetime | None = None) -> int:
    event_repo = PostgresEventRepository(dsn=dsn)
    label_repo = PostgresLabelRepository(dsn=dsn)
    impressions = event_repo.read_impressions(since=since)
    actions = event_repo.read_user_actions(since=since)

    actions_by_key: dict[tuple[str, str], list[str]] = defaultdict(list)
    for action in actions:
        actions_by_key[(action.search_id, action.property_id)].append(action.action_type)

    base_labels: dict[tuple[str, str], RankingLabel] = {}
    for impression in impressions:
        key = (impression.search_id, impression.property_id)
        relevance, source = compute_label(
            actions_for_property=actions_by_key.get(key, []),
            impression_present=True,
        )
        if source == "no_impression":
            continue
        base_labels[key] = RankingLabel(
            search_id=impression.search_id,
            property_id=impression.property_id,
            relevance_label=relevance,
            label_source=source,
        )

    synthetic_labels = inject_synthetic_labels(
        base_labels=base_labels,
        actions_by_key=actions_by_key,
        fixture_path=fixture_path,
    )
    merged = dict(base_labels)
    for label in synthetic_labels:
        key = (label.search_id, label.property_id)
        existing = merged.get(key)
        if existing is None or label.relevance_label > existing.relevance_label:
            merged[key] = label

    label_repo.write_ranking_labels(list(merged.values()))
    return len(merged)


def main() -> None:
    settings = TrainSettings()
    fixture_path = Path("definitions/labeling/synthetic_actions.yaml")
    since = datetime.now(UTC) - timedelta(days=settings.training_window_days)
    count = run(dsn=settings.postgres_dsn, fixture_path=fixture_path, since=since)
    logger.info("labeling_job done: labels=%d", count)


if __name__ == "__main__":
    main()
