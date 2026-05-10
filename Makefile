SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

# Absolute paths keep targets idempotent regardless of invocation cwd.
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
TF_DIR := $(ROOT)/infra/terraform/environments/dev

# Project-wide non-credential settings live in env/config/setting.yaml so
# Python (scripts/_common.py) and Make read from one source of truth. We
# parse the flat key:value file with awk (faster than `uv run python` and
# already a Make hard dep for the help target).
SETTINGS_FILE := $(ROOT)/env/config/setting.yaml
_yaml_get = $(strip $(shell awk -F: '/^$(1):/ {gsub(/^[ "'\'']+|[ "'\'']+$$/,"",$$2); print $$2; exit}' $(SETTINGS_FILE)))

PROJECT_ID    ?= $(call _yaml_get,project_id)
REGION        ?= $(call _yaml_get,region)
API_SERVICE   ?= $(call _yaml_get,api_service)
ARTIFACT_REPO ?= $(call _yaml_get,artifact_repo)
VERTEX_LOCATION ?= $(call _yaml_get,vertex_location)
PIPELINE_ROOT_BUCKET ?= $(call _yaml_get,pipeline_root_bucket)
PIPELINE_TEMPLATE_GCS_PATH ?= $(call _yaml_get,pipeline_template_gcs_path)
COMPOSER_ENV  ?= hybrid-search-orchestrator

# Override-able via CLI: `make tf-plan GITHUB_REPO=other/repo ONCALL_EMAIL=...`
GITHUB_REPO   ?= $(call _yaml_get,github_repo)
ONCALL_EMAIL  ?= $(call _yaml_get,oncall_email)

# Local model path produced by `make train-smoke-persist`.
MODEL_PATH_OVERRIDE ?= /tmp/hybrid-search-cloud-smoke-model.txt

# deploy / verification log output directories.
LOG_ROOT ?= $(ROOT)/logs
MONITOR_LOG_DIR ?= $(LOG_ROOT)/deploy-monitor
VERIFY_LOG_DIR ?= $(LOG_ROOT)/verification

PHASE_NAME := phase-7-gke
NA_TARGETS := up down wait-db free-ports build seed serve test-e2e install-browsers \
	db-migrate-% db-seed-% ops-bootstrap \
	ops-sync ops-embed ops-train-build ops-train-fit ops-ranking-verbose \
	ops-weekly \
	eval-compare eval-offline kpi-daily eval-weekly-report features-daily features-report \
	api-dev-search-rerank setup-encoder-endpoint setup-reranker-endpoint \
	ops-monitor ops-monitor-lro ops-enable-search

include mk/base.mk

export PROJECT_ID REGION API_SERVICE ARTIFACT_REPO VERTEX_LOCATION PIPELINE_ROOT_BUCKET PIPELINE_TEMPLATE_GCS_PATH

.PHONY: help doctor sync sync-app sync-ml sync-pipelines test lint fmt fmt-check typecheck check \
        check-layers sync-dataform-config sync-configmap \
	tf-bootstrap tf-init tf-validate tf-fmt tf-fmt-fix tf-plan \
	setup-model-monitoring \
        setup-pipeline-schedule \
        apply-manifests \
        deploy-all deploy-all-direct run-all destroy-all seed-test seed-test-clean \
	verify-deploy-all verify-destroy-all verify-live-acceptance verify-full-recreate \
        sync-elasticsearch sync-synonyms \
        label-build build-training-dataset train-smoke train-smoke-persist api-dev api-dev-hybrid \
        verify-local-parity verify-local-app verify-local-ml verify-local-hybrid clean \
        docker-auth build-ml-base-local deploy-api deploy-api-local deploy-kserve-images deploy-kserve-images-local deploy-kserve-models kube-creds \
        composer-deploy-dags build-composer-runner ops-composer-trigger ops-composer-list-runs ops-composer-task-states \
		ops-deploy-monitor \
        ops-api-url ops-daily ops-livez ops-search ops-search-components ops-ranking ops-feedback \
        ops-accuracy-report local-accuracy-report \
        ops-skew-latest ops-search-volume ops-runs-recent \
	ops-skew-run ops-train-now ops-train-wait ops-pipeline-run ops-promote-reranker ops-reload-api \
	ops-check-retrain ops-bq-scan-top ops-label-seed \
        ops-slo-status bqml-train-popularity \
        ops-kserve-monitoring ops-destroy-check \
        ops-vertex-models-list ops-vertex-pipeline-status ops-vertex-explain \
        ops-vertex-monitoring ops-vertex-vector-search-smoke ops-vertex-feature-group \
        ops-vertex-all

help: ## Show this help
	@uv run python -u -m scripts.lib.makefile_help $(MAKEFILE_LIST)

doctor: ## Verify that prerequisite tools are installed
	uv run python -u -m scripts.setup.doctor

# ----- Python workspace -----

sync: ## uv sync (full workspace: root package + dev group + all extras: ml, pipelines)
	uv sync --dev --all-extras

sync-app: ## uv sync for app-centric local work (base deps + dev only)
	uv sync --dev

sync-ml: ## uv sync for local ML work (base deps + dev + ml extra)
	uv sync --dev --extra ml-encoder --extra ml-reranker --extra ml-train

sync-pipelines: ## uv sync for local pipeline work (base deps + dev + ml + pipelines extras)
	uv sync --dev --extra ml-train --extra pipelines

test: ## Run pytest across the workspace
	uv run pytest

lint: ## ruff check
	uv run ruff check .

fmt: ## ruff format (writes)
	uv run ruff format .

fmt-check: ## ruff format --check
	uv run ruff format --check .

typecheck: ## mypy strict
	uv run mypy app ml pipeline

check: lint fmt-check typecheck test ## Run all CI-equivalent checks

sync-dataform-config: ## Regenerate pipeline/data_job/dataform/workflow_settings.yaml
	uv run python -u -m scripts.ci.sync_dataform

sync-configmap: ## Regenerate infra/manifests/search-api/configmap.example.yaml from setting.yaml
	uv run python -u -m scripts.ci.sync_configmap

check-layers: ## AST-based layer boundary check (Ports / pure logic must not import concrete adapters or SDKs)
	uv run python -u -m scripts.ci.layers

# ----- Terraform -----

tf-bootstrap: ## Phase 0: enable APIs + create tfstate bucket (idempotent, needs project owner rights)
	uv run python -u -m scripts.setup.tf_bootstrap

tf-init: ## terraform init (with tfstate bucket preflight check)
	uv run python -u -m scripts.setup.tf_init

tf-validate: ## terraform validate (backend-less, works offline)
	terraform -chdir=$(TF_DIR) init -backend=false -upgrade=false >/dev/null
	terraform -chdir=$(TF_DIR) validate

tf-fmt: ## terraform fmt --check
	terraform -chdir=$(TF_DIR) fmt -check -diff

tf-fmt-fix: ## terraform fmt (writes)
	terraform -chdir=$(TF_DIR) fmt

tf-plan: ## terraform plan (requires GITHUB_REPO + ONCALL_EMAIL; saves tfplan)
	uv run python -u -m scripts.setup.tf_plan

setup-model-monitoring: ## Print resolved Vertex Model Monitoring setup payload
	uv run python -u -m scripts.setup.setup_model_monitoring

setup-pipeline-schedule: ## Print resolved Vertex Pipeline schedule setup payload
	uv run python -u -m scripts.setup.create_schedule

apply-manifests: ## Apply infra/manifests via kubectl apply -k
	kubectl apply -k $(ROOT)/infra/manifests

deploy-all: ## End-to-end provisioning + search-api rollout (tf-apply → kubectl apply -k → overlay-configmap → deploy-api)
	uv run python -u -m scripts.setup.deploy_all

verify-deploy-all: ## Run deploy-all and aggregate stdout/stderr under logs/verification/
	uv run python -u -m scripts.verify.deploy_all

state-recover: ## Import orphan GCP resources back into tfstate (緊急 cleanup 後の "alreadyExists" fail 回避、`docs/tasks/TASKS_ROADMAP.md §4.10`)
	uv run python -u -m scripts.domain.gcp.state_recovery

ops-deploy-monitor: ## Real-time monitor: runs deploy-all and reports live step/build stall status
	uv run python -u -m scripts.deploy.monitor --label deploy-monitor

deploy-all-direct: ## Compatibility alias of deploy-all (Phase4 naming)
	$(MAKE) deploy-all

run-all: ## End-to-end validation flow after deploy (layer check → seed → train pipeline submit → smoke APIs → daily ops)
	$(MAKE) ops-run-all-monitor

run-all-core: ## Core validation flow after deploy (no monitor wrapper)
	$(MAKE) check-layers
	$(MAKE) seed-test
	$(MAKE) sync-elasticsearch
	$(MAKE) ops-train-now
	$(MAKE) ops-train-wait
	$(MAKE) ops-livez
	$(MAKE) ops-search
	$(MAKE) ops-search-components
	$(MAKE) ops-vertex-vector-search-smoke
	$(MAKE) ops-vertex-feature-group
	$(MAKE) ops-feedback
	$(MAKE) ops-ranking
	$(MAKE) ops-label-seed
	$(MAKE) ops-daily
	$(MAKE) ops-accuracy-report

ops-run-all-monitor: ## Real-time monitor for run-all-core
	uv run python -u -m scripts.deploy.monitor --label run-all -- make run-all-core

verify-all: ## Alias of run-all-core for cross-phase teaching vocabulary
	$(MAKE) run-all-core

destroy-all: ## Tear down every Terraform-managed resource (no prompt — PDCA loop, pair with deploy-all)
	uv run python -u -m scripts.setup.destroy_all

verify-destroy-all: ## Run destroy-all and aggregate stdout/stderr under logs/verification/
	uv run python -u -m scripts.verify.destroy_all

verify-live-acceptance: ## Run canonical live acceptance and aggregate logs under logs/verification/
	uv run python -u -m scripts.verify.live_acceptance

verify-full-recreate: ## Run destroy-all -> deploy-all -> live acceptance gate and aggregate logs under logs/verification/
	uv run python -u -m scripts.verify.full_recreate

ops-destroy-check: ## Assert no high-cost residual Phase 7 resources remain after destroy-all
	uv run python -u -m scripts.ops.destroy_check --project-id=$(PROJECT_ID) --region=$(REGION) --vertex-location=$(VERTEX_LOCATION)

destroy-phase7-learning: ## Coast-down placeholder: Dataflow Job / Feature Online Store / KServe explain pod
	@echo "Not implemented yet. See docs/runbook/05_運用.md for current manual coast-down guidance."
	@exit 1

seed-test: ## Insert 5 test properties for PDCA smoke
	uv run python -u -m scripts.setup.seed_minimal

seed-test-clean: ## Drop the test seed data (benign if absent)
	uv run python -u -m scripts.setup.seed_minimal_clean

sync-synonyms: ## Sync synonym dictionary YAML -> Cloud Memorystore for Redis (skips when Memorystore not provisioned)
	uv run python -u -m scripts.ops.sync_synonyms

sync-elasticsearch: ## Sync feature_mart.properties_cleaned -> Elasticsearch (canonical lexical lane)
	uv run python -u -m scripts.ops.sync_elasticsearch \
		--project-id=$(PROJECT_ID) \
		--es-url=$${ELASTICSEARCH_URL:-http://elasticsearch.search.svc.cluster.local:9200}

# ----- App / Job smoke commands (local) -----

label-build: ## Materialize ranking_labels from search_impressions + user_actions
	uv run python -m pipeline.labeling_job.main

build-training-dataset: ## Export ranking_labels-based training dataset CSV under dist/training_datasets
	uv run python -m pipeline.training_dataset_job.main

train-smoke: ## Dry-run the ranker training job locally (synthetic data, no GCS/BQ)
	uv run --extra ml-train rank-train --dry-run

train-smoke-persist: ## Dry-run ranker trainer and copy the model to $(MODEL_PATH_OVERRIDE)
	uv run --extra ml-train rank-train --dry-run --save-to "$(MODEL_PATH_OVERRIDE)"

api-dev: ## Start uvicorn locally (rerank-free /search requires ENABLE_SEARCH=1 + BQ creds)
	ENABLE_SEARCH=false uv run uvicorn app.main:app --reload

api-dev-hybrid: ## Start local-first hybrid stack (app + local encoder/reranker + Elasticsearch if reachable)
	env UV_CACHE_DIR=/tmp/uv-cache uv run --extra ml-encoder --extra ml-reranker python -m scripts.setup.local_hybrid

verify-local-parity: ## Offline parity + codebase invariants (no GCP; catches doc/spec drift in CI)
	uv run pytest tests/integration/parity -q

verify-local-app: ## Fast local app loop (layer check + app/script unit tests, no live GCP)
	$(MAKE) check-layers
	uv run ruff check app tests/unit/app tests/unit/scripts/test_local_hybrid.py scripts/setup/local_hybrid.py scripts/deploy/api_gke_local.py scripts/deploy/build_kserve_images_local.py
	uv run ruff format --check app tests/unit/app tests/unit/scripts/test_local_hybrid.py scripts/setup/local_hybrid.py scripts/deploy/api_gke_local.py scripts/deploy/build_kserve_images_local.py
	uv run mypy app scripts/setup/local_hybrid.py scripts/deploy/api_gke_local.py scripts/deploy/build_kserve_images_local.py
	uv run pytest tests/unit/app tests/unit/scripts/test_local_hybrid.py -q

verify-local-ml: ## Fast local ML loop (ML/pipeline unit tests + smoke train, no deploy)
	uv run ruff check ml pipeline tests/unit/ml tests/unit/pipeline
	uv run ruff format --check ml pipeline tests/unit/ml tests/unit/pipeline
	uv run mypy ml pipeline
	uv run --extra ml-train --extra pipelines pytest tests/unit/ml tests/unit/pipeline -q
	$(MAKE) train-smoke

verify-local-hybrid: ## Local hybrid loop (parity + contract + app + ML; avoids deploy-all/run-all live steps)
	$(MAKE) verify-local-parity
	uv run pytest tests/integration/workflow/test_ground_truth_contract.py -q
	$(MAKE) verify-local-app
	$(MAKE) verify-local-ml

# ----- Local deploy path (bypasses CI; uses Cloud Build + kubectl) -----

docker-auth: ## (Optional) configure local docker for Artifact Registry
	gcloud auth configure-docker $(REGION)-docker.pkg.dev --quiet

build-ml-base-local: ## Local docker buildx cache base for encoder/reranker builder stages
	docker buildx build --file infra/run/services/ml_base/Dockerfile --load -t phase7-ml-base:local .

kube-creds: ## Fetch kubeconfig for the GKE Autopilot cluster
	gcloud container clusters get-credentials $${GKE_CLUSTER_NAME:-hybrid-search} --region=$(REGION) --project=$(PROJECT_ID)

deploy-api: ## Cloud Build (kaniko cache) + `kubectl set image` for search-api
	uv run python -u -m scripts.deploy.api_gke

deploy-api-local: ## ローカル docker buildx + push + rollout (BuildKit cache mount で 2 回目以降が高速)
	uv run python -u -m scripts.deploy.api_gke_local

deploy-kserve-images: ## Cloud Build + image patch for property-encoder/reranker InferenceServices
	uv run python -u -m scripts.deploy.build_kserve_images

deploy-kserve-images-local: ## Local docker buildx + push + cluster patch for encoder/reranker
	uv run python -u -m scripts.deploy.build_kserve_images_local

deploy-kserve-models: ## Sync Model Registry artifacts into KServe InferenceService
	uv run python -u -m scripts.deploy.kserve_models

composer-deploy-dags: ## Upload pipeline/dags/*.py to Composer DAG GCS bucket (Phase 7 W2-4)
	uv run python -u -m scripts.deploy.composer_deploy_dags

build-composer-runner: ## Cloud Build composer-runner image (DAG KubernetesPodOperator runner、V5 fix)
	uv run python -u -m scripts.deploy.composer_runner

# Canonical backend remains `gcloud composer environments run ...` wrapped by
# Python modules so Make targets stay one-line and contract-testable.
ops-composer-trigger: ## Trigger a Composer DAG manually (DAG=retrain_orchestration etc.)
	DAG=$(DAG) uv run python -u -m scripts.ops.composer_dag trigger

ops-composer-list-runs: ## List recent runs of a Composer DAG (DAG=retrain_orchestration etc.)
	DAG=$(DAG) uv run python -u -m scripts.ops.composer_dag list-runs

ops-composer-task-states: ## Task states for latest run (DAG=...) or RUN_ID=manual__...
	DAG=$(DAG) RUN_ID=$(RUN_ID) uv run python -u -m scripts.ops.composer_task_states

seed-lgbm-model: ## Seed a synthetic LightGBM model into gs://$(MODELS_BUCKET)/lgbm/latest/ (idempotent)
	uv run python -u -m scripts.deploy.seed_lgbm_model

# ----- Housekeeping -----

clean: ## Remove caches (.venv, .terraform, pyc)
	rm -rf .venv $(TF_DIR)/.terraform
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache -o -name .mypy_cache \) -prune -exec rm -rf {} +

# ----- GCP operations (see docs/runbook/05_運用.md §3) -----

ops-api-url: ## Print the search-api Gateway external URL
	@kubectl get gateway search-api-gateway --namespace=search -o jsonpath='{.status.addresses[0].value}' 2>/dev/null | sed -e 's|^|https://|' -e 's|$$||' || echo "search-api-gateway not yet provisioned"

ops-daily: ops-skew-latest ops-search-volume ops-runs-recent ## Run the 3 core daily checks

ops-skew-latest: ## Today's per-feature skew detection results (validation_results)
	bq query --use_legacy_sql=false --project_id=$(PROJECT_ID) < scripts/sql/skew_latest.sql

ops-search-volume: ## /search request volume over the last 24h
	bq query --use_legacy_sql=false --project_id=$(PROJECT_ID) < scripts/sql/search_volume.sql

ops-runs-recent: ## Last 5 LightGBM LambdaRank training runs
	bq query --use_legacy_sql=false --project_id=$(PROJECT_ID) < scripts/sql/runs_recent.sql

ops-skew-run: ## Ad-hoc execution of infra/sql/monitoring/validate_feature_skew.sql
	bq query --use_legacy_sql=false --project_id=$(PROJECT_ID) < infra/sql/infra/sql/monitoring/validate_feature_skew.sql

ops-bq-scan-top: ## Top 20 BQ scans in the last 7 days (cost audit)
	bq query --use_legacy_sql=false --project_id=$(PROJECT_ID) < scripts/sql/bq_scan_top.sql

ops-recover-wif: ## Manually reconcile WIF pool/provider with Terraform state (PDCA loop safety)
	uv run python -u -m scripts.setup.recover_wif

ops-train-now: ## Submit train pipeline to Vertex AI
	uv run python -m pipeline.workflow.compile --target train --output-dir dist/pipelines --submit --project-id $(PROJECT_ID) --location $(VERTEX_LOCATION) --pipeline-root gs://$(PIPELINE_ROOT_BUCKET)/runs --service-account sa-pipeline@$(PROJECT_ID).iam.gserviceaccount.com

ops-train-wait: ## Wait for the latest train pipeline run to reach SUCCEEDED
	uv run python -u -m scripts.ops.vertex.pipeline_wait

ops-pipeline-run: ## Submit a pipeline manually: TARGET=embed|train PARAM='key=value'
	uv run python -m pipeline.workflow.compile --target $${TARGET:-train} --output-dir dist/pipelines --submit --project-id $(PROJECT_ID) --location $(VERTEX_LOCATION) --pipeline-root gs://$(PIPELINE_ROOT_BUCKET)/runs --service-account sa-pipeline@$(PROJECT_ID).iam.gserviceaccount.com $${PARAM:+--parameter $$PARAM}

ops-promote-reranker: ## Promote a reranker to `production` alias. Usage: MODEL_ID=N or VERSION_ID=N [BST_RENAME=1] [APPLY=1].
	uv run python -u -m scripts.ops.promote reranker

ops-promote-encoder: ## Promote an encoder to `production` alias. Usage: MODEL_ID=N or VERSION_ID=N [APPLY=1].
	uv run python -u -m scripts.ops.promote encoder

ops-reload-api: ## Trigger a rolling restart of search-api Pods to re-read ConfigMap / model URIs
	kubectl rollout restart deployment/search-api --namespace=search

ops-livez: ## Hit /livez on the deployed search-api (IAM-gated)
	uv run python -u -m scripts.ops.livez

ops-search: ## POST /search smoke (override QUERY/TOP_K/MAX_RENT env vars)
	uv run python -u -m scripts.ops.search

ops-search-components: ## Strict gate: lexical/semantic/rerank contributions must all be non-zero
	uv run python -u -m scripts.ops.search_components

ops-ranking: ## POST /search and inspect lexical_rank / final_rank / score / me5_score
	uv run python -u -m scripts.ops.ranking

ops-feedback: ## /search → /feedback round-trip (publisher path smoke)
	uv run python -u -m scripts.ops.feedback

ops-label-seed: ## Seed canonical user actions against /search
	uv run python -u -m scripts.ops.label_seed

ops-check-retrain: ## POST /jobs/check-retrain with OIDC; pipe to jq
	uv run python -u -m scripts.ops.check_retrain

ops-accuracy-report: ## Simple ranking accuracy report on deployed Cloud Run (/search, TARGET=gcp)
	TARGET=gcp uv run python -u -m scripts.ops.accuracy_report

local-accuracy-report: ## Simple ranking accuracy report against local API (/search, TARGET=local)
	TARGET=local uv run python -u -m scripts.ops.accuracy_report

# ----- Phase 6 PMLE ops targets -----

ops-slo-status: ## Phase 6 T5: print current compliance + burn-rate (1h/3d) for availability + latency SLOs
	uv run python -u -m scripts.ops.slo_status

bqml-train-popularity: ## Phase 6 T1: train BQML property-popularity model (BOOSTED_TREE_REGRESSOR)
	uv run python -u -m scripts.bqml.train_popularity

# ----- Vertex AI feature verification scripts (each ops target probes one Vertex
# AI surface in isolation. ops-vertex-all chains them; individual ones are useful
# when triaging which surface broke.)

ops-vertex-models-list: ## Vertex Model Registry: list versions/aliases for encoder/reranker
	uv run python -u -m scripts.ops.vertex.models_list

ops-vertex-pipeline-status: ## Vertex Pipelines: list latest runs + state (LIMIT=10)
	uv run python -u -m scripts.ops.vertex.pipeline_status

ops-vertex-explain: ## Vertex Explainable AI via /search?explain=true (assert non-empty attributions)
	uv run python -u -m scripts.ops.vertex.explain

ops-vertex-monitoring: ## Vertex Model Monitoring: read recent BQ alert rows (LIMIT=10)
	uv run python -u -m scripts.ops.vertex.monitoring

ops-kserve-monitoring: ## Phase 7 self-managed drift alerts from model_monitoring_alerts (LIMIT=10)
	uv run python -u -m scripts.ops.vertex.monitoring

ops-vertex-vector-search-smoke: ## Vertex Vector Search: probe find_neighbors against the live serving index
	uv run python -u -m scripts.ops.vertex.vector_search

ops-vertex-feature-group: ## Vertex Feature Group: fetch online feature values for PROPERTY_ID=p001
	uv run python -u -m scripts.ops.vertex.feature_group

ops-vertex-all: ops-vertex-models-list ops-vertex-pipeline-status ops-vertex-explain ops-vertex-monitoring ops-vertex-vector-search-smoke ops-vertex-feature-group ## Run every Vertex AI smoke check in sequence
	@echo "==> all Vertex AI smoke checks completed"
