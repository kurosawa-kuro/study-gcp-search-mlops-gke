from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

from app.services.adapters.bigquery_event_repository import BigQueryEventRepository
from app.services.adapters.bigquery_label_repository import BigQueryLabelRepository
from app.domain.labeling import RankingLabel


def _result_with_rows(*rows: dict[str, object]) -> MagicMock:
    job = MagicMock()
    job.result.return_value = list(rows)
    return job


def test_bigquery_event_repository_reads_search_events_with_since_param() -> None:
    client = MagicMock()
    client.query.return_value = _result_with_rows(
        {
            "search_id": "s-1",
            "query": "渋谷 1LDK",
            "filters_json": {"max_rent": 200000},
            "user_id": "u-1",
            "session_id": "sess-1",
            "app_version": "v1",
            "model_version": "model-a",
            "timestamp": datetime(2026, 5, 6, tzinfo=timezone.utc),
        }
    )
    repo = BigQueryEventRepository(
        client=client,
        search_events_table="p.mlops.search_events",
        search_impressions_table="p.mlops.search_impressions",
        user_actions_table="p.mlops.user_actions",
    )

    rows = repo.read_search_events(since=datetime(2026, 5, 1, tzinfo=timezone.utc))

    assert len(rows) == 1
    assert rows[0].search_id == "s-1"
    assert rows[0].filters_json == '{"max_rent": 200000}'
    job_config = client.query.call_args.kwargs["job_config"]
    params = {param.name: param.value for param in job_config.query_parameters}
    assert params["since"].year == 2026
    assert "WHERE timestamp >= @since" in client.query.call_args.args[0]


def test_bigquery_event_repository_reads_impressions_and_user_actions() -> None:
    client = MagicMock()
    client.query.side_effect = [
        _result_with_rows(
            {
                "search_id": "s-2",
                "property_id": "P-001",
                "rank": 1,
                "lexical_rank_orig": 2,
                "semantic_rank_orig": 3,
                "lexical_score": None,
                "vector_score": 0.88,
                "rrf_score": 0.91,
                "rerank_score": 1.2,
                "timestamp": datetime(2026, 5, 6, tzinfo=timezone.utc),
            }
        ),
        _result_with_rows(
            {
                "search_id": "s-2",
                "property_id": "P-001",
                "action_type": "request_complete",
                "action_value": 1.0,
                "timestamp": datetime(2026, 5, 6, tzinfo=timezone.utc),
            }
        ),
    ]
    repo = BigQueryEventRepository(
        client=client,
        search_events_table="p.mlops.search_events",
        search_impressions_table="p.mlops.search_impressions",
        user_actions_table="p.mlops.user_actions",
    )

    impressions = repo.read_impressions(search_id="s-2")
    actions = repo.read_user_actions(search_id="s-2", action_type="request_complete")

    assert impressions[0].property_id == "P-001"
    assert impressions[0].rerank_score == 1.2
    assert actions[0].action_type == "request_complete"
    assert actions[0].action_value == 1.0


def test_bigquery_label_repository_write_ranking_labels_merges_rows() -> None:
    client = MagicMock()
    client.query.return_value = _result_with_rows()
    repo = BigQueryLabelRepository(
        client=client,
        ranking_labels_table="p.mlops.ranking_labels",
    )

    repo.write_ranking_labels(
        [
            RankingLabel(
                search_id="s-3",
                property_id="P-010",
                relevance_label=5,
                label_source="request_complete",
            )
        ]
    )

    sql = client.query.call_args.args[0]
    assert "MERGE `p.mlops.ranking_labels`" in sql
    params = client.query.call_args.kwargs["job_config"].query_parameters
    values = {param.name: param.value for param in params}
    assert values["search_id"] == "s-3"
    assert values["relevance_label"] == 5
    assert values["label_source"] == "request_complete"


def test_bigquery_label_repository_reads_labels() -> None:
    client = MagicMock()
    client.query.return_value = _result_with_rows(
        {
            "search_id": "s-4",
            "property_id": "P-011",
            "relevance_label": 3,
            "label_source": "favorite",
            "created_at": datetime(2026, 5, 6, tzinfo=timezone.utc),
        }
    )
    repo = BigQueryLabelRepository(
        client=client,
        ranking_labels_table="p.mlops.ranking_labels",
    )

    labels = repo.read_ranking_labels()

    assert len(labels) == 1
    assert labels[0].search_id == "s-4"
    assert labels[0].relevance_label == 3
    assert labels[0].label_source == "favorite"
