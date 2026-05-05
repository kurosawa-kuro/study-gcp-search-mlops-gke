from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime, timedelta

from google.cloud import bigquery

from app.domain.labeling import RankingLabel
from app.services.adapters.bigquery_event_repository import BigQueryEventRepository
from app.services.adapters.bigquery_label_repository import BigQueryLabelRepository
from ml.common import get_logger
from ml.common.config import TrainSettings
from ml.labeling import compute_label

logger = get_logger("pipeline.labeling_job")


def run(*, window_days: int = 90) -> int:
    settings = TrainSettings()
    client = bigquery.Client(project=settings.project_id)
    mlops_prefix = f"{settings.project_id}.{settings.bq_dataset_mlops}"
    event_repo = BigQueryEventRepository(
        client=client,
        search_events_table=f"{mlops_prefix}.search_events",
        search_impressions_table=f"{mlops_prefix}.search_impressions",
        user_actions_table=f"{mlops_prefix}.user_actions",
    )
    label_repo = BigQueryLabelRepository(
        client=client,
        ranking_labels_table=f"{mlops_prefix}.ranking_labels",
    )
    since = datetime.now(UTC) - timedelta(days=window_days)
    impressions = event_repo.read_impressions(since=since)
    actions = event_repo.read_user_actions(since=since)

    actions_by_key: dict[tuple[str, str], list[str]] = defaultdict(list)
    for action in actions:
        actions_by_key[(action.search_id, action.property_id)].append(action.action_type)

    labels: list[RankingLabel] = []
    for impression in impressions:
        key = (impression.search_id, impression.property_id)
        relevance, source = compute_label(
            actions_for_property=actions_by_key.get(key, []),
            impression_present=True,
        )
        if source == "no_impression":
            continue
        labels.append(
            RankingLabel(
                search_id=impression.search_id,
                property_id=impression.property_id,
                relevance_label=relevance,
                label_source=source,
            )
        )

    label_repo.write_ranking_labels(labels)
    logger.info("labeling_job done: labels=%d window_days=%d", len(labels), window_days)
    return len(labels)


def main() -> None:
    run()


if __name__ == "__main__":
    main()
