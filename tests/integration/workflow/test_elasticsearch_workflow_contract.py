"""Elasticsearch workflow contract for Phase 7 canonical lexical lane.

Guard rails for regressions where deploy/run flows stop syncing lexical docs
or drift back to removed Meilisearch-era wiring.
"""

from __future__ import annotations

import re

from tests.integration.workflow.conftest import read_repo_file as _read


def test_makefile_exposes_sync_elasticsearch_canonical_target() -> None:
    makefile = _read("Makefile")
    assert (
        "sync-elasticsearch: ## Sync feature_mart.properties_cleaned -> Elasticsearch" in makefile
    )
    assert "uv run python -m scripts.ops.sync_elasticsearch" in makefile


def test_run_all_core_keeps_sync_elasticsearch_before_search_smokes() -> None:
    makefile = _read("Makefile")
    run_all_core_match = re.search(
        r"^run-all-core:.*?(?=^\S|^$)",
        makefile,
        flags=re.DOTALL | re.MULTILINE,
    )
    assert run_all_core_match is not None, "run-all-core target not found in Makefile"
    recipe = run_all_core_match.group(0)
    assert "$(MAKE) sync-elasticsearch" in recipe, (
        "run-all-core must sync lexical index before search smoke checks"
    )
    assert recipe.index("$(MAKE) sync-elasticsearch") < recipe.index("$(MAKE) ops-search"), (
        "sync-elasticsearch must run before ops-search in run-all-core"
    )


def test_deploy_all_sync_elasticsearch_step_wiring_stays_canonical() -> None:
    deploy_all_py = _read("scripts/setup/deploy_all.py")

    assert (
        "from scripts.ops.sync_elasticsearch import run as sync_elasticsearch_run" in deploy_all_py
    )
    assert 'DeployStep(\n            10,\n            "sync-elasticsearch",' in deploy_all_py
    assert "canonical lexical path" in deploy_all_py
    assert '"http://elasticsearch.search.svc.cluster.local:9200"' in deploy_all_py
    assert 'f"--project-id={project_id}"' in deploy_all_py
    assert 'f"--es-url={es_url}"' in deploy_all_py


def test_docs_runbook_and_catalog_pin_elasticsearch_workflow() -> None:
    runbook = _read("docs/runbook/05_運用.md")
    catalog = _read("docs/architecture/03_実装カタログ.md")
    readme = _read("README.md")

    assert "sync-elasticsearch" in runbook
    assert "sync-elasticsearch" in catalog
    assert "Elasticsearch" in readme

    for body in (runbook, catalog, readme):
        assert "Meilisearch" not in body
        assert "sync-meili" not in body
