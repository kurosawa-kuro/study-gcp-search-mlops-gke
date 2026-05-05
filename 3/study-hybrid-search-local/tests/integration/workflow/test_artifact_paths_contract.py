"""Phase 3 workflow contract — artifact / dataset path invariants."""

from __future__ import annotations

from pathlib import Path

from ml.registry.artifact_store import LocalArtifactStore
from tests.integration.workflow.conftest import read_repo_file as _read


def test_local_artifact_store_pins_latest_symlink_layout(tmp_path: Path) -> None:
    store = LocalArtifactStore(root=tmp_path)

    run_dir = store.run_dir("run-001")
    latest = store.update_latest("run-001")

    assert run_dir == tmp_path / "run-001"
    assert latest == tmp_path / "latest"
    assert latest.is_symlink()
    assert latest.resolve() == run_dir.resolve()


def test_training_dataset_job_pins_datasets_runid_csv_layout() -> None:
    source = _read("pipeline/training_dataset_job/main.py")
    for required in (
        "root = Path(settings.model_artifacts_root)",
        'output_dir = root / "datasets" / run_id',
        'output_path = output_dir / "training_dataset.csv"',
    ):
        assert required in source, f"training dataset path contract drifted: {required}"


def test_evaluation_job_pins_latest_model_and_metrics_sidecar() -> None:
    source = _read("pipeline/evaluation_job/main.py")
    for required in (
        'latest = artifacts_root / "latest" / "model.lgb"',
        'metrics_json_path = model_path.parent / "metrics.json"',
        'artifacts_root = Path(os.environ.get("MODEL_ARTIFACTS_ROOT", "ml/registry/artifacts"))',
    ):
        assert required in source, f"evaluation artifact contract drifted: {required}"


def test_model_data_router_pins_latest_training_dataset_preview() -> None:
    source = _read("app/api/routers/model_router.py")
    for required in (
        'dataset_root = root / "datasets"',
        'candidates = sorted(dataset_root.glob("*/training_dataset.csv"), reverse=True)',
        "table_fqn=str(latest)",
    ):
        assert required in source, f"/model/data preview contract drifted: {required}"
