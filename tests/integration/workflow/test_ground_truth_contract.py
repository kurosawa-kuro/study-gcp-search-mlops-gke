"""Workflow contract for Phase 7 ground-truth data path.

Pins the canonical path introduced from Phase 3:

1. `/search` emits `search_events` and `search_impressions`
2. `/feedback` emits `user_actions`
3. `label-build` materializes `ranking_labels`
4. `build-training-dataset` exports a dataset derived from `ranking_labels`
5. Vertex train pipeline consumes `ranking_labels` + `search_impressions`
"""

from __future__ import annotations

from tests.integration.workflow.conftest import read_repo_file as _read


def test_makefile_exposes_ground_truth_targets() -> None:
    makefile = _read("Makefile")

    for required in (
        "label-build: ## Materialize ranking_labels from search_impressions + user_actions",
        "build-training-dataset: ## Export ranking_labels-based training dataset CSV under dist/training_datasets",
        "ops-label-seed: ## Seed canonical user actions against /search",
        "build-ml-base-local: ## Local docker buildx cache base for encoder/reranker builder stages",
        "verify-local-parity: ## Offline parity + codebase invariants (no GCP; catches doc/spec drift in CI)",
        "verify-local-app: ## Fast local app loop (layer check + app/script unit tests, no live GCP)",
        "verify-local-ml: ## Fast local ML loop (ML/pipeline unit tests + smoke train, no deploy)",
        "verify-local-hybrid: ## Local hybrid loop (parity + contract + app + ML; avoids deploy-all/run-all live steps)",
        "sync-app: ## uv sync for app-centric local work (base deps + dev only)",
        "sync-ml: ## uv sync for local ML work (base deps + dev + ml extra)",
        "sync-pipelines: ## uv sync for local pipeline work (base deps + dev + ml + pipelines extras)",
    ):
        assert required in makefile, f"Makefile lost ground-truth target: {required}"
    for required in (
        "uv sync --dev --extra ml-encoder --extra ml-reranker --extra ml-train",
        "uv sync --dev --extra ml-train --extra pipelines",
        "uv run --extra ml-train rank-train --dry-run",
        "uv run --extra ml-encoder --extra ml-reranker python -m scripts.setup.local_hybrid",
        "docker buildx build --file infra/run/services/ml_base/Dockerfile --load -t phase7-ml-base:local .",
    ):
        assert required in makefile, f"Makefile lost local-build optimization contract: {required}"


def test_kserve_dockerfiles_use_split_ml_extras() -> None:
    ml_base_dockerfile = _read("infra/run/services/ml_base/Dockerfile")
    encoder_dockerfile = _read("infra/run/services/encoder/Dockerfile")
    reranker_dockerfile = _read("infra/run/services/reranker/Dockerfile")

    assert "uv sync --frozen --no-dev --no-install-project" in ml_base_dockerfile
    assert "ARG ML_BUILDER_IMAGE" in encoder_dockerfile
    assert "--extra ml-encoder --no-install-project" in encoder_dockerfile
    assert "ARG ML_BUILDER_IMAGE" in reranker_dockerfile
    assert "--extra ml-reranker --no-install-project" in reranker_dockerfile
    assert "--mount=type=cache,target=/var/cache/apt,sharing=locked" in reranker_dockerfile


def test_training_pipeline_contract_uses_ranking_labels_not_feedback_events() -> None:
    pipeline_main = _read("pipeline/training_job/main.py")
    load_features = _read("pipeline/training_job/components/load_features.py")
    workflow_compile = _read("pipeline/workflow/compile.py")
    ranker_repo = _read("ml/data/loaders/ranker_repository.py")

    for required in (
        'search_impressions_table: str = "search_impressions"',
        'ranking_labels_table: str = "ranking_labels"',
    ):
        assert required in pipeline_main

    assert '"search_impressions_table": "search_impressions"' in workflow_compile
    assert '"ranking_labels_table": "ranking_labels"' in workflow_compile
    assert "FROM `{project_id}.{mlops_dataset_id}.{ranking_labels_table}` rl" in load_features
    assert "JOIN `{project_id}.{mlops_dataset_id}.{search_impressions_table}` si" in load_features
    assert "FROM `{ranking_labels}` rl" in ranker_repo
    assert "JOIN `{search_impressions}` si" in ranker_repo
    assert "feedback_events_table" not in pipeline_main


def test_dataform_and_app_contract_use_canonical_event_schema() -> None:
    dataform = _read("pipeline/data_job/dataform/features/property_features_daily.sqlx")
    feedback_schema = _read("app/schemas/search.py")
    feedback_panel = _read("app/templates/_feedback_panel.html")
    event_writer = _read("app/services/adapters/cloud_logging_event_writer.py")

    assert '${ref("search_impressions")}' in dataform
    assert '${ref("user_actions")}' in dataform
    assert 'COUNTIF(action_type = "request_complete")' in dataform
    for action in (
        '"detail_view"',
        '"request_button_click"',
        '"request_complete"',
    ):
        assert action in feedback_schema
    for option in (
        'option value="detail_view"',
        'option value="request_button_click"',
        'option value="request_complete"',
    ):
        assert option in feedback_panel
    for event_name in (
        '"event_name": "search_event"',
        '"event_name": "search_impression"',
        '"event_name": "user_action"',
    ):
        assert event_name in event_writer
