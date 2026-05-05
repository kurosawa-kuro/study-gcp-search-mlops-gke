"""Phase 3 app / UI integration checks.

Preconditions:
- ``make up``
- ``make seed``
- ``make train``
- ``docker compose up -d search-api``
"""

from __future__ import annotations

import os

import httpx
import pytest

API_BASE = os.environ.get("PHASE3_API_BASE", "http://localhost:8000")


def _api_alive() -> bool:
    try:
        response = httpx.get(f"{API_BASE}/health", timeout=2.0)
        return response.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _api_alive(),
    reason=f"Phase 3 search-api not reachable at {API_BASE} (run `make verify-app` or start search-api first)",
)


def test_ui_pages_return_200() -> None:
    pages = [
        "/ui/",
        "/ui/dev/model/metrics",
        "/ui/dev/data",
        "/ui/property/prop-0001",
    ]
    with httpx.Client(base_url=API_BASE, timeout=10.0, follow_redirects=True) as client:
        for path in pages:
            response = client.get(path)
            assert response.status_code == 200, f"{path} failed: {response.text[:200]}"


def test_model_endpoints_return_expected_payloads() -> None:
    with httpx.Client(base_url=API_BASE, timeout=20.0) as client:
        info = client.get("/model/info")
        assert info.status_code == 200, info.text
        info_payload = info.json()
        assert info_payload["search_enabled"] is True
        assert info_payload["rerank_enabled"] is True
        assert info_payload["reranker_model_path"]

        metrics = client.get("/model/metrics")
        assert metrics.status_code == 200, metrics.text
        metrics_payload = metrics.json()
        assert metrics_payload["num_cases"] >= 1
        assert 0.0 <= metrics_payload["summary"]["ndcg_at_k"] <= 1.0
        assert metrics_payload["per_case"], "per_case should not be empty"

        data = client.get("/model/data")
        assert data.status_code == 200, data.text
        tables = {table["key"]: table for table in data.json()["tables"]}
        assert {"feature-mart", "ranking-labels", "search-impressions", "training-dataset"} <= set(
            tables
        )
        assert tables["feature-mart"]["rows"], "feature-mart preview should not be empty"
        assert tables["search-impressions"]["columns"], "search-impressions preview missing columns"
