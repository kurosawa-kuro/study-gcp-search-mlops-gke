from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_setup_scripts_use_canonical_and_ci_import_paths() -> None:
    deploy_all = _read("scripts/setup/deploy_all.py")
    destroy_all = _read("scripts/setup/destroy_all.py")

    assert "from scripts.ci.sync_dataform import main as sync_dataform_main" in deploy_all
    assert "from scripts.deploy.api_gke import main as deploy_api_main" in deploy_all
    assert "from scripts.setup.tf_bootstrap import main as tf_bootstrap_main" in deploy_all
    assert "from scripts.setup.tf_init import main as tf_init_main" in deploy_all
    assert "from scripts.setup.tf_plan import main as tf_plan_main" in deploy_all

    assert "from scripts.setup.seed_minimal_clean import main as seed_clean_main" in destroy_all


def test_setup_scripts_target_dev_terraform_environment() -> None:
    # 2026-05-09 refactor: tf-apply の business logic は scripts/setup/tf_apply.py
    # に分離 (deploy_all.py は orchestrator のみ)。INFRA 定数の所在も移動。
    destroy_all = _read("scripts/setup/destroy_all.py")
    tf_init = _read("scripts/setup/tf_init.py")
    tf_plan = _read("scripts/setup/tf_plan.py")
    tf_apply = _read("scripts/setup/tf_apply.py")

    expected = (
        'Path(__file__).resolve().parents[2] / "infra" / "terraform" / "environments" / "dev"'
    )
    assert expected in destroy_all
    assert expected in tf_init
    assert expected in tf_plan
    assert expected in tf_apply


def test_api_deploy_targets_gke_rollout_path() -> None:
    api_gke = _read("scripts/deploy/api_gke.py")

    assert "kubectl" in api_gke
    assert "rollout status" in api_gke
    assert "deployment/search-api" in api_gke or 'DEPLOYMENT = "search-api"' in api_gke
    assert "gcloud run deploy" not in api_gke


def test_makefile_has_canonical_ops_targets() -> None:
    makefile = _read("Makefile")

    assert "deploy-all-direct:" in makefile
    assert "ops-search-components:" in makefile
    assert "ops-accuracy-report:" in makefile
    assert "local-accuracy-report:" in makefile
    assert "python -u -m scripts.ops.search_components" in makefile
    assert "python -u -m scripts.ops.accuracy_report" in makefile


def test_makefile_sync_elasticsearch_passes_required_args() -> None:
    """2026-05-09 incident: bare `make sync-elasticsearch` failed with
    `--es-url / ELASTICSEARCH_URL is empty` because the Makefile target did not
    forward `--project-id` or `--es-url`. The deploy-all path worked because
    `_run_sync_elasticsearch` builds the args explicitly, but the make target
    itself was unusable for individual step retry — exactly the slicing
    workflow user prefers (`細かく確実に`).

    Pin: the make target must forward both args, with `ELASTICSEARCH_URL`
    falling back to the canonical cluster-local URL.
    """
    makefile = _read("Makefile")

    assert "--project-id=$(PROJECT_ID)" in makefile, (
        "sync-elasticsearch target must forward --project-id from $(PROJECT_ID)"
    )
    assert (
        "ELASTICSEARCH_URL:-http://elasticsearch.search.svc.cluster.local:9200"
        in makefile
    ), (
        "sync-elasticsearch target must use canonical cluster-local URL as fallback "
        "when ELASTICSEARCH_URL is unset"
    )


def test_seed_and_feature_group_contract_pin_feature_timestamp() -> None:
    seed_minimal = _read("scripts/setup/seed_minimal.py")
    data_tf = _read("infra/terraform/modules/data/main.tf")
    vertex_tf = _read("infra/terraform/modules/vertex/main.tf")

    assert "feature_timestamp" in data_tf
    assert "Feature-time column required by Vertex AI Feature Group BigQuery source" in data_tf
    assert "CURRENT_TIMESTAMP()" in seed_minimal
    assert "feature_timestamp, property_id" in seed_minimal
    assert 'entity_id_columns = ["property_id"]' in vertex_tf
