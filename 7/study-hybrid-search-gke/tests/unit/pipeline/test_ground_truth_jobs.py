from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.domain.event import Impression, UserAction
from app.domain.labeling import RankingLabel


def test_labeling_job_builds_labels_from_impressions_and_actions(monkeypatch) -> None:
    from pipeline.labeling_job import main as module

    written: list[RankingLabel] = []

    class _FakeEventRepository:
        def read_impressions(self, *, since=None):  # type: ignore[no-untyped-def]
            return [
                Impression(
                    search_id="s-1",
                    property_id="P-001",
                    rank=1,
                    lexical_rank_orig=1,
                    semantic_rank_orig=1,
                    lexical_score=None,
                    vector_score=0.8,
                    rrf_score=None,
                    rerank_score=1.1,
                ),
                Impression(
                    search_id="s-1",
                    property_id="P-002",
                    rank=2,
                    lexical_rank_orig=2,
                    semantic_rank_orig=2,
                    lexical_score=None,
                    vector_score=0.5,
                    rrf_score=None,
                    rerank_score=0.7,
                ),
            ]

        def read_user_actions(self, *, since=None):  # type: ignore[no-untyped-def]
            return [
                UserAction(
                    search_id="s-1",
                    property_id="P-001",
                    action_type="request_complete",
                    action_value=1.0,
                ),
                UserAction(
                    search_id="s-1",
                    property_id="P-002",
                    action_type="click",
                    action_value=None,
                ),
            ]

    class _FakeLabelRepository:
        def write_ranking_labels(self, labels: list[RankingLabel]) -> None:
            written.extend(labels)

    monkeypatch.setattr(module, "BigQueryEventRepository", lambda **kwargs: _FakeEventRepository())
    monkeypatch.setattr(module, "BigQueryLabelRepository", lambda **kwargs: _FakeLabelRepository())
    monkeypatch.setattr(
        module,
        "TrainSettings",
        lambda: type(
            "S",
            (),
            {"project_id": "p", "bq_dataset_mlops": "mlops"},
        )(),
    )
    monkeypatch.setattr(module.bigquery, "Client", lambda project: object())

    count = module.run(window_days=30)

    assert count == 2
    assert {(label.property_id, label.relevance_label) for label in written} == {
        ("P-001", 5),
        ("P-002", 1),
    }


def test_training_dataset_job_exports_relevance_label_csv(
    monkeypatch, tmp_path: Path
) -> None:
    from pipeline.training_dataset_job import main as module

    frame = pd.DataFrame(
        [
            {
                "request_id": "s-1",
                "property_id": "P-001",
                "label": 5,
                "rent": 120000,
                "walk_min": 5,
                "age_years": 10,
                "area_m2": 30.0,
                "ctr": 0.1,
                "fav_rate": 0.02,
                "inquiry_rate": 0.01,
                "me5_score": 0.9,
                "lexical_rank": 1.0,
                "semantic_rank": 1.0,
            }
        ]
    )

    class _FakeRepository:
        def fetch_training_rows(self, *, window_days: int) -> pd.DataFrame:
            assert window_days == 14
            return frame.copy()

    monkeypatch.setattr(module, "create_rank_repository", lambda settings: _FakeRepository())
    monkeypatch.setattr(module, "generate_run_id", lambda: "run-123")
    monkeypatch.setattr(module, "TrainSettings", lambda: object())

    output = module.run(window_days=14, output_root=tmp_path)

    assert output == tmp_path / "run-123" / "training_dataset.csv"
    body = output.read_text(encoding="utf-8")
    header = body.splitlines()[0]
    assert "relevance_label" in header
    assert ",label," not in f",{header},"
