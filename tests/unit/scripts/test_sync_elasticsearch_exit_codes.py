"""Exit-code contract for ``scripts.ops.sync_elasticsearch``.

Programmatic callers (deploy-all) must receive shell-style codes: ``0`` ok,
``1`` validation failure — not a row count (historical bug).
"""

from __future__ import annotations

import pytest

from scripts.ops import sync_elasticsearch as sync_es


def test_run_returns_one_when_project_id_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PROJECT_ID", raising=False)
    assert sync_es.run(["--es-url=http://127.0.0.1:9200"]) == 1


def test_run_returns_one_when_es_url_missing() -> None:
    assert sync_es.run(["--project-id=any-project"]) == 1
