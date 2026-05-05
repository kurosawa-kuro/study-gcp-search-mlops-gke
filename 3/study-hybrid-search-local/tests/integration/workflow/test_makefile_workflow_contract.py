"""Phase 3 workflow contract — Makefile canonical validation path."""

from __future__ import annotations

from tests.integration.workflow.conftest import read_repo_file as _read


def _target_block(makefile: str, target: str) -> str:
    start = makefile.index(f"{target}:")
    next_target = makefile.find("\n\n", start)
    return makefile[start:] if next_target == -1 else makefile[start:next_target]


def test_verify_all_core_recipe_pins_canonical_validation_order() -> None:
    makefile = _read("Makefile")
    block = _target_block(makefile, "verify-all-core")
    expected_lines = [
        "$(MAKE) check",
        "$(MAKE) check-layers",
        "$(MAKE) verify-contracts",
        "$(MAKE) build",
        "$(MAKE) up",
        "$(MAKE) seed",
        "$(MAKE) train",
        "$(MAKE) verify-app",
        "$(MAKE) verify-ml",
    ]
    positions = [block.index(line) for line in expected_lines]
    assert positions == sorted(positions), (
        "verify-all-core drifted from the canonical Phase 3 validation order"
    )
    assert "verify-all: ## verify-all-core の alias" in makefile
    assert "run-all-core: ## verify-all-core の alias" in makefile
    assert "$(MAKE) verify-all-core" in makefile


def test_seed_recipe_pins_seed_then_synonym_sync() -> None:
    makefile = _read("Makefile")
    block = _target_block(makefile, "seed")
    seed_run = "$(COMPOSE) run --rm seed"
    seed_synonyms = "$(MAKE) seed-synonyms"
    assert block.index(seed_run) < block.index(seed_synonyms), (
        "seed must run before seed-synonyms so Redis gets a dataset-aligned dictionary"
    )


def test_verify_app_recipe_pins_api_ui_contract() -> None:
    makefile = _read("Makefile")
    block = _target_block(makefile, "verify-app")
    required_lines = [
        "verify-app: ## app / API / UI の総合疎通 (serve 起動込み)",
        "$(MAKE) serve-bg",
        "$(MAKE) wait-api",
        "uv run pytest tests/integration/test_pipeline_e2e.py tests/integration/test_app_ui_e2e.py -q",
    ]
    for required in required_lines:
        assert required in block, f"verify-app lost contract line: {required}"


def test_up_recipe_pins_wait_then_idempotent_migration() -> None:
    makefile = _read("Makefile")
    block = _target_block(makefile, "up")
    expected_lines = [
        "$(COMPOSE) up -d postgres meilisearch redis",
        "@$(MAKE) wait-db",
        "@$(MAKE) migrate-db",
    ]
    positions = [block.index(line) for line in expected_lines]
    assert positions == sorted(positions), (
        "up must wait for postgres before re-applying idempotent migrations"
    )


def test_verify_ml_recipe_pins_feedback_to_metrics_path() -> None:
    makefile = _read("Makefile")
    block = _target_block(makefile, "verify-ml")
    expected_lines = [
        "$(MAKE) label",
        "$(MAKE) build-training-dataset",
        "$(MAKE) train",
        "$(MAKE) evaluate",
        "uv run pytest tests/integration/test_ml_feedback_cycle_e2e.py -q",
    ]
    positions = [block.index(line) for line in expected_lines]
    assert positions == sorted(positions), (
        "verify-ml must keep the label -> dataset -> train -> evaluate path"
    )


def test_migrate_db_recipe_replays_all_sql_files() -> None:
    makefile = _read("Makefile")
    block = _target_block(makefile, "migrate-db")
    assert "ls /docker-entrypoint-initdb.d/*.sql | sort" in block
    assert 'psql -U admin -d hybrid_search -v ON_ERROR_STOP=1 -f "$$f"' in block
