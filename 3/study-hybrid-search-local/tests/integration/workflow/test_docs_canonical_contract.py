"""Phase 3 workflow contract — docs canonical wording + command parity."""

from __future__ import annotations

from tests.integration.workflow.conftest import read_repo_file as _read


def test_readme_exposes_phase3_verification_entrypoints() -> None:
    readme = _read("README.md")
    for required in (
        "make serve-bg && make wait-api",
        "make verify-app",
        "make verify-ml",
        "make verify-all",
        "/ui/dev/model/metrics",
        "/ui/dev/data",
    ):
        assert required in readme, f"README lost verification entrypoint: {required}"


def test_runbooks_pin_phase3_canonical_validation_flow() -> None:
    validation = _read("docs/runbook/04_検証.md")
    operations = _read("docs/runbook/05_運用.md")

    for required in (
        "V1-V6",
        "make verify-app",
        "make verify-ml",
        "make verify-all",
        "/ui/dev/model/metrics",
        "/ui/dev/data",
        "training_dataset.csv",
        "metrics.json",
    ):
        assert required in validation, f"validation guide lost canonical gate: {required}"

    for required in (
        "make serve-bg",
        "make wait-api",
        "make verify-app",
        "make verify-ml",
        "make verify-all",
        "prop-0001",
        "<searchのrequest_id>",
    ):
        assert required in operations, (
            f"operations guide drifted from workflow contract: {required}"
        )


def test_implementation_catalog_mentions_workflow_contract_inventory() -> None:
    catalog = _read("docs/architecture/03_実装カタログ.md")
    for required in (
        "tests/integration/workflow/",
        "make verify-contracts",
        "make verify-app",
        "make verify-ml",
        "make verify-all",
    ):
        assert required in catalog, (
            f"implementation catalog drifted from workflow/test inventory: {required}"
        )
