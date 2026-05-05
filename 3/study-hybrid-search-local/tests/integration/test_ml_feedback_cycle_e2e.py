"""Phase 3 Wave 5-7 integration checks.

Preconditions:
- ``make verify-app`` already created search / feedback rows
- ``make label``
- ``make build-training-dataset``
- ``make train``
- ``make evaluate``
"""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import httpx
import psycopg
import pytest

API_BASE = os.environ.get("PHASE3_API_BASE", "http://localhost:8000")
POSTGRES_DSN = os.environ.get(
    "PHASE3_POSTGRES_DSN",
    "postgresql://admin:password@localhost:5433/hybrid_search",
)
ARTIFACTS_ROOT = Path(
    os.environ.get(
        "PHASE3_ARTIFACTS_ROOT",
        "/home/ubuntu/repos/study-gcp-search-mlops-gke/3/study-hybrid-search-local/ml/registry/artifacts",
    )
)


def _api_alive() -> bool:
    try:
        response = httpx.get(f"{API_BASE}/health", timeout=2.0)
        return response.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _api_alive(),
    reason=f"Phase 3 search-api not reachable at {API_BASE} (run `make verify-ml` after app startup)",
)


def _count(table: str) -> int:
    with psycopg.connect(POSTGRES_DSN) as conn, conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        row = cur.fetchone()
        assert row is not None
        return int(row[0])


def _latest_dataset_csv() -> Path:
    candidates = sorted((ARTIFACTS_ROOT / "datasets").glob("*/training_dataset.csv"), reverse=True)
    assert candidates, "training_dataset.csv not found"
    return candidates[0]


def test_search_and_feedback_persist_wave57_rows() -> None:
    before_events = _count("search_events")
    before_impressions = _count("search_impressions")
    before_actions = _count("user_actions")

    search_payload = {
        "query": "新宿区西新宿 1LDK",
        "filters": {"max_rent": 150000},
        "top_k": 5,
    }
    with httpx.Client(base_url=API_BASE, timeout=20.0) as client:
        search = client.post("/search", json=search_payload)
        assert search.status_code == 200, search.text
        search_body = search.json()
        assert search_body["results"], "search returned no results"
        request_id = search_body["request_id"]
        property_id = search_body["results"][0]["property_id"]

        feedback = client.post(
            "/feedback",
            json={
                "request_id": request_id,
                "property_id": property_id,
                "action": "click",
            },
        )
        assert feedback.status_code == 200, feedback.text
        assert feedback.json()["accepted"] is True

    assert _count("search_events") >= before_events + 1
    assert _count("search_impressions") >= before_impressions + 1
    assert _count("user_actions") >= before_actions + 1


def test_label_dataset_metrics_artifacts_exist() -> None:
    assert _count("ranking_labels") >= 1, "ranking_labels should exist after make label"

    dataset = _latest_dataset_csv()
    with dataset.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        first_row = next(reader, None)
    assert first_row is not None, "training_dataset.csv should contain rows"
    assert "relevance_label" in first_row

    latest_dir = ARTIFACTS_ROOT / "latest"
    assert (latest_dir / "model.lgb").exists(), "latest/model.lgb missing"
    metrics_file = latest_dir / "metrics.json"
    assert metrics_file.exists(), "latest/metrics.json missing"
    metrics = json.loads(metrics_file.read_text(encoding="utf-8"))
    assert "ndcg_at_10" in metrics
    assert "map" in metrics
    assert "recall_at_20" in metrics


def test_model_data_preview_shows_generated_training_dataset() -> None:
    response = httpx.get(f"{API_BASE}/model/data", timeout=15.0)
    assert response.status_code == 200, response.text
    tables = {table["key"]: table for table in response.json()["tables"]}
    dataset_table = tables["training-dataset"]
    assert dataset_table["rows"], "training-dataset preview should contain rows"
    assert dataset_table["table_fqn"].endswith("training_dataset.csv")
