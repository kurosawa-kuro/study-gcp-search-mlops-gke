"""Phase 7 workflow contract - local verification path and canonical endpoint wiring.

This file guards the fast local loop that should stay independent from the
live-GCP ``deploy-all`` / ``run-all`` path while still exercising the same
public / ops HTTP contracts.
"""

from __future__ import annotations

from tests.integration.workflow.conftest import read_repo_file as _read


def test_verify_local_hybrid_recipe_pins_fast_local_order() -> None:
    """``verify-local-hybrid`` must stay a thin local loop.

    Contract:
    1. ground-truth workflow contract first
    2. app-local loop second
    3. ml-local loop third
    4. no live-GCP targets (`deploy-all` / `run-all`) mixed in
    """
    makefile = _read("Makefile")
    expected_lines = [
        "uv run pytest tests/integration/workflow/test_ground_truth_contract.py -q",
        "$(MAKE) verify-local-app",
        "$(MAKE) verify-local-ml",
    ]
    positions = [makefile.index(line) for line in expected_lines]
    assert positions == sorted(positions), (
        "verify-local-hybrid drifted from the canonical local validation order"
    )

    block_start = makefile.index("verify-local-hybrid:")
    next_target = makefile.find("\n\n", block_start)
    block = makefile[block_start : next_target if next_target != -1 else None]
    recipe_lines = [line.strip() for line in block.splitlines() if line.startswith("\t")]
    recipe = "\n".join(recipe_lines)
    assert "deploy-all" not in recipe
    assert "run-all" not in recipe


def test_verify_local_app_contract_pins_local_only_scope() -> None:
    makefile = _read("Makefile")
    for required in (
        "uv run ruff check app tests/unit/app tests/unit/scripts/test_local_hybrid.py",
        "uv run ruff format --check app tests/unit/app tests/unit/scripts/test_local_hybrid.py",
        "uv run mypy app scripts/setup/local_hybrid.py scripts/deploy/api_gke_local.py scripts/deploy/build_kserve_images_local.py",
        "uv run pytest tests/unit/app tests/unit/scripts/test_local_hybrid.py -q",
    ):
        assert required in makefile, f"verify-local-app lost local contract: {required}"


def test_verify_local_ml_contract_pins_local_only_scope() -> None:
    makefile = _read("Makefile")
    for required in (
        "uv run ruff check ml pipeline tests/unit/ml tests/unit/pipeline",
        "uv run ruff format --check ml pipeline tests/unit/ml tests/unit/pipeline",
        "uv run mypy ml pipeline",
        "uv run --extra ml-train --extra pipelines pytest tests/unit/ml tests/unit/pipeline -q",
        "$(MAKE) train-smoke",
    ):
        assert required in makefile, f"verify-local-ml lost local contract: {required}"


def test_ui_templates_fetch_canonical_api_v1_and_ops_paths() -> None:
    search_dev = _read("app/templates/search_dev.html")
    data_html = _read("app/templates/data.html")
    metrics_html = _read("app/templates/model_metrics.html")
    property_detail = _read("app/templates/property_detail.html")
    search_ui = _read("app/static/js/search_ui.js")

    assert "`/ops/model/info`" in search_dev
    assert 'fetch("/ops/model/data")' in data_html
    assert "fetch(`/ops/model/metrics?k=${k}`)" in metrics_html
    assert 'fetch("/api/v1/feedback"' in property_detail

    for required in (
        '"/api/v1/search?explain=true"',
        '"/api/v1/search"',
        'fetch("/api/v1/feedback"',
        'fetch("/ops/model/info")',
    ):
        assert required in search_ui, f"search_ui.js lost canonical fetch path: {required}"


def test_ops_scripts_use_canonical_api_v1_and_ops_paths() -> None:
    expectations = {
        "scripts/ops/search.py": [
            'target.call("POST", "/api/v1/search"',
        ],
        "scripts/ops/feedback.py": [
            'target.call("POST", "/api/v1/search"',
            '"/api/v1/feedback"',
        ],
        "scripts/ops/check_retrain.py": [
            'target.call("POST", "/ops/jobs/check-retrain")',
        ],
        "scripts/ops/search_components.py": [
            'resolved.call("POST", "/api/v1/search"',
        ],
        "scripts/ops/ranking.py": [
            'target.call("POST", "/api/v1/search"',
        ],
        "scripts/ops/label_seed.py": [
            'target.call("POST", "/api/v1/search"',
            '"/api/v1/feedback"',
        ],
        "scripts/ops/accuracy_report.py": [
            'resolved.call("POST", "/api/v1/search"',
        ],
    }
    for rel, required_list in expectations.items():
        body = _read(rel)
        for required in required_list:
            assert required in body, f"{rel} lost canonical endpoint contract: {required}"


def test_readme_documents_local_verification_entrypoints() -> None:
    readme = _read("README.md")
    for required in (
        "make verify-local-app",
        "make verify-local-ml",
        "make verify-local-hybrid",
        "make deploy-all",
        "make run-all",
        "make destroy-all",
    ):
        assert required in readme, f"README lost workflow entrypoint: {required}"
