SHELL := /usr/bin/env bash
.DEFAULT_GOAL := help

ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,uv run python)
COMPOSE := docker compose

PHASE_NAME := phase-3-local
# Phase 3 ではクラウド系 / KServe / Composer / Vertex / BQML 系は N/A。
NA_TARGETS := \
	tf-bootstrap tf-init tf-validate tf-fmt tf-fmt-fix tf-plan \
	deploy-all deploy-all-direct deploy-api deploy-api-local deploy-training-job-local deploy-kserve-models destroy-all \
	setup-encoder-endpoint setup-reranker-endpoint setup-model-monitoring setup-pipeline-schedule \
	ops-monitor ops-monitor-lro ops-monitor-deploy \
	ops-livez ops-search ops-search-components ops-ranking ops-ranking-verbose \
	ops-feedback ops-label-seed ops-accuracy-report ops-daily ops-weekly \
	ops-sync ops-embed ops-train-build ops-train-fit ops-train-now ops-pipeline-run \
	ops-reload-api ops-enable-search ops-promote-reranker ops-check-retrain \
	ops-api-url ops-skew-latest ops-skew-run ops-search-volume ops-runs-recent \
	ops-bq-scan-top ops-slo-status \
	bqml-train-popularity enrich-properties destroy-phase6-learning kube-creds \
	eval-compare eval-offline kpi-daily eval-weekly-report features-daily features-report \
	api-dev-search-rerank ops-bootstrap

include ../../mk/base.mk

.PHONY: help doctor sync build build-api build-jobs up migrate-db warm-model seed train label build-training-dataset evaluate serve serve-bg api-dev test check check-layers \
	wait-db wait-api verify-contracts verify-pipeline verify-app verify-ml verify-all-core run-all-core run-all verify-all down clean

help: ## Show this help
	@echo "Phase 3 (Local hybrid search) — quick start: make build && make up && make seed && make train && make serve-bg && make wait-api"
	@echo "Full verification: make verify-all"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} \
		/^[a-zA-Z0-9_-]+:.*##/ { printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2 }' \
		$(MAKEFILE_LIST)

doctor: ## Verify prerequisite tools (uv / docker / make)
	@command -v uv >/dev/null 2>&1 && echo "  ✓ uv" || (echo "  ✗ uv not found"; exit 1)
	@command -v docker >/dev/null 2>&1 && echo "  ✓ docker" || (echo "  ✗ docker not found"; exit 1)
	@$(COMPOSE) version >/dev/null 2>&1 && echo "  ✓ docker compose" || (echo "  ✗ docker compose not found"; exit 1)

sync: ## uv workspace + dev group 同期
	uv sync --all-extras --dev

build: ## Build all app/job Docker images
	$(MAKE) build-jobs
	$(MAKE) build-api

build-jobs: ## Build shared pipeline job image once (seed / trainer / labeler / evaluator)
	$(COMPOSE) build seed

build-api: ## Build search-api image
	$(COMPOSE) build search-api

up: ## docker compose up -d (postgres / meilisearch / redis のみ起動 + idempotent migration)
	$(COMPOSE) up -d postgres meilisearch redis
	@$(MAKE) wait-db
	@$(MAKE) migrate-db

migrate-db: ## postgres migration を既存 volume に再適用 (idempotent)
	@echo "Applying postgres migrations"
	@$(COMPOSE) exec -T postgres sh -lc 'set -eu; for f in $$(ls /docker-entrypoint-initdb.d/*.sql | sort); do echo "  -> $$f"; psql -U admin -d hybrid_search -v ON_ERROR_STOP=1 -f "$$f"; done'

wait-db: ## postgres healthcheck PASS まで待つ
	@printf "Waiting postgres "
	@for i in $$(seq 1 30); do \
		if $(COMPOSE) exec -T postgres pg_isready -U admin -d hybrid_search >/dev/null 2>&1; then \
			echo " OK"; exit 0; \
		fi; \
		printf "."; sleep 1; \
	done; \
	echo " timeout"; exit 1

seed: ## synthetic 不動産データ + 同義語辞書 を全 backend に投入
	$(COMPOSE) run --rm seed
	$(MAKE) seed-synonyms

warm-model: ## multilingual-e5 を共有 hf_cache に事前取得
	$(MAKE) build-jobs
	$(COMPOSE) run --rm model-warmup

seed-synonyms: ## 同義語辞書 → Redis SET (lexical query expansion 用)
	$(COMPOSE) run --rm seed-synonyms

train: ## LightGBM LambdaRank 学習 → ml/registry/artifacts/{run_id}/model.lgb
	$(COMPOSE) run --rm trainer

label: ## search_impressions × user_actions → ranking_labels
	$(COMPOSE) run --rm labeler

build-training-dataset: ## ranking_labels 由来の training dataset CSV を出力
	$(COMPOSE) run --rm training-dataset-builder

evaluate: ## NDCG@10 / MAP / Recall@20 の hold-out 評価 → metrics.json
	$(COMPOSE) run --rm evaluator

serve: ## search-api を :8000 で起動 (foreground)
	$(COMPOSE) up search-api

serve-bg: ## search-api を :8000 で起動 (background)
	$(COMPOSE) up -d search-api

wait-api: ## search-api /health が 200 になるまで待つ
	@printf "Waiting search-api "
	@for i in $$(seq 1 60); do \
		if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then \
			echo " OK"; exit 0; \
		fi; \
		printf "."; sleep 1; \
	done; \
	echo " timeout"; exit 1

api-dev: ## ローカル uvicorn (Docker なし、uv run。前提: postgres/meili/redis は up 済)
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test: ## pytest 全体 (ローカル)
	uv run pytest tests/unit -q

check: ## ローカル CI 同等 (ruff + ruff format --check + mypy + pytest)
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy app ml pipeline
	uv run pytest tests/unit -q

check-layers: ## Port-Adapter 境界の AST 検査
	uv run python -m scripts.ci.layers

verify-contracts: ## Makefile / docs / artifact path の workflow contract 検証
	uv run pytest tests/integration/workflow -q

verify-pipeline: ## seed → train → serve の integration E2E (docker compose 立ち上げ済前提)
	uv run pytest tests/integration -q

verify-app: ## app / API / UI の総合疎通 (serve 起動込み)
	$(MAKE) serve-bg
	$(MAKE) wait-api
	uv run pytest tests/integration/test_pipeline_e2e.py tests/integration/test_app_ui_e2e.py -q

verify-ml: ## feedback → labeling → dataset → retrain → evaluate の ML 経路検証
	$(MAKE) label
	$(MAKE) build-training-dataset
	$(MAKE) train
	$(MAKE) evaluate
	uv run pytest tests/integration/test_ml_feedback_cycle_e2e.py -q

verify-all-core: ## 静的検証 + local stack + app + ML 経路を 1 コマンドで
	$(MAKE) check
	$(MAKE) check-layers
	$(MAKE) verify-contracts
	$(MAKE) build
	$(MAKE) up
	$(MAKE) seed
	$(MAKE) train
	$(MAKE) verify-app
	$(MAKE) verify-ml

run-all-core: ## verify-all-core の alias
	$(MAKE) verify-all-core

run-all: ## run-all-core の alias
	$(MAKE) run-all-core

verify-all: ## verify-all-core の alias (Phase 横断 vocabulary)
	$(MAKE) verify-all-core

down: ## docker compose down (volume 残す)
	$(COMPOSE) down --remove-orphans

clean: ## down + 生成物削除 (model artifacts / volumes)
	$(COMPOSE) down --remove-orphans --volumes
	rm -rf ml/registry/artifacts/*
