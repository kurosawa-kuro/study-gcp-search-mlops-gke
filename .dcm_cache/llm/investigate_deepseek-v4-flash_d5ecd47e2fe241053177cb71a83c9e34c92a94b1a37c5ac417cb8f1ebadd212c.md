# Investigated Findings

generated_by: dcm investigate
source: non_llm_evidence_investigation
judgment_status: llm_enriched

## observed_signals

- Evidence Pack exists and has the required scan, symbol, config, risk, and scan-limitation files. evidence_ref: file=evidence/00_scan_manifest.md
- Symbol evidence exists for code navigation and candidate responsibility boundaries. evidence_ref: file=evidence/03_symbols.md
- Configuration and environment evidence exists for secret and runtime-risk review. evidence_ref: file=evidence/08_config_env.md
- Static signal evidence exists and must be investigated before draft. evidence_ref: file=evidence/30_static_signal_hits.md
- Scan limitation evidence exists and can inform descriptive current implications when judgment-relevant. evidence_ref: file=evidence/99_scan_limitations.md

## available_evidence_files

- `00_evidence_freshness.md`
- `00_scan_manifest.md`
- `01_file_tree.md`
- `02_files.json`
- `03_symbols.md`
- `04_symbols.json`
- `05_tests.md`
- `07_entrypoints.md`
- `08_config_env.md`
- `09_diff_evidence.md`
- `10_observed_change_signals.json`
- `10_observed_change_signals.md`
- `11_dependency_inventory.json`
- `11_dependency_inventory.md`
- `12_code_metrics.json`
- `12_code_metrics.md`
- `13_public_api_surface.json`
- `13_public_api_surface.md`
- `14_code_excerpts.json`
- `14_code_excerpts.md`
- `15_decision_memory.json`
- `15_decision_memory.md`
- `30_static_signal_hits.md`
- `98_redaction_report.md`
- `99_scan_limitations.md`

## llm_enrichment

## item_meaning_candidates

- **Config env variables** – The inventory of environment variables (e.g., `AIP_STORAGE_URI`, `ENCODER_MODEL_NAME`, `ELASTICSEARCH_URL`, `REDIS_AUTH`) indicates the system is heavily parameterised at runtime, with per-service overrides for ML model serving (KServe), lexical search (Elasticsearch), synonym expansion (Redis), and GCP project/region identity.  
  *Evidence_ref*: `evidence/08_config_env.md`

- **Static signal hits** – High counts for `env_secret` (613), `high_risk_ops` (602), `auth_permission` (759), and `infra_surface` (1620) suggest the codebase contains a significant surface area of privileged operations, secret management, and infrastructure manipulation. These signals are observations only, not decisions.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md`

- **Change signals** – Frequent changes to `docs/tasks/TASKS_ROADMAP.md`, `docs/architecture/03_実装カタログ.md`, and `CLAUDE.md` imply ongoing architectural documentation and roadmap evolution, likely reflecting active development.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md` (change_signal rows, `evidence/10_observed_change_signals.md` not fully provided but referenced)

- **Symbol structure** – The large symbol set (3188 symbols, 888 tests) across Python, TypeScript, CSS, HTML, Terraform, Docker, and shell scripts indicates a polyglot project with deep test coverage. The presence of both `noop_adapters` and real adapters (e.g., PubSub, BigQuery, KServe) suggests a clean architecture pattern with testable interfaces.  
  *Evidence_ref*: `evidence/00_scan_manifest.md`, `evidence/03_symbols.md`

- **Domain objects** – Classes like `RankedCandidate`, `SearchEvent`, `TrainingDatasetRef`, `EvaluationMetric` define core data flow entities, while `ContainerBuilder` and `InfraBuilder` show dependency injection patterns for GCP services.  
  *Evidence_ref*: `evidence/03_symbols.md`

## role_notes

- **`app/` – API and search orchestration**  
  FastAPI routers, middleware, service layer, and adapters implement the search API, feedback, ops endpoints, and model management. The `container/` directory manages dependency injection for GCP clients (BigQuery, PubSub, Vertex AI).  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `app/api/routers/`, `app/container/`, `app/services/adapters/`)

- **`ml/` – ML model serving and training**  
  Encoder and reranker KServe inference services (E5, LightGBM), training pipelines, experiment tracking, and registry management. Includes `streaming/` for Dataflow-based click-stream processing.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `ml/serving/`, `ml/training/`, `ml/streaming/`)

- **`pipeline/` – Orchestrated ML pipelines**  
  Composer DAGs, KFP pipeline compilation, batch serving and evaluation jobs, labeling, and training. Uses modular components (`training_job/`, `data_job/`, etc.).  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `pipeline/dags/`, `pipeline/training_job/`)

- **`scripts/` – Deployment, ops, and infrastructure management**  
  Shell-like Python scripts for terraform apply, GCP resource recovery, ES sync, model promotion, and full lifecycle (deploy_all, destroy_all).  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `scripts/deploy/`, `scripts/ops/`, `scripts/setup/`)

- **`infra/terraform/` – Infrastructure as Code**  
  Terraform modules for GKE, Cloud Composer, Vertex AI, BigQuery, PubSub, IAM, DNS, monitoring/SLOs, and Redis synonym store.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `infra/terraform/modules/*/main.tf`)

- **`tests/` – Multi-layer test suite**  
  Unit tests (`tests/unit/`), integration tests (`tests/integration/`), e2e acceptance tests (`tests/e2e/`), and in-memory fakes/stubs for controller-style testing.  
  *Evidence_ref*: `evidence/00_scan_manifest.md` (test_count: 888), `evidence/03_symbols.md` (tests/ section)

## current_implications

- **Active development documented in change signals** – The roadmap and architectural docs have recent modifications, implying the system is still evolving. Changes to `TASKS_ROADMAP.md` and architecture catalogs suggest ongoing refactoring or feature work.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md` (change_signal:docs/tasks/TASKS_ROADMAP.md, etc.)

- **High test coverage (888 tests) enables confident refactoring** – The project has unit, integration, and e2e tests covering API contract, infrastructure invariants, data pipeline wiring, and ML metrics. This reduces risk when modifying core logic.  
  *Evidence_ref*: `evidence/00_scan_manifest.md` (test_count: 888)

- **Production readiness indicated by SLOs, monitoring, and retrain policies** – Terraform modules for SLO alerts, logging metrics, BigQuery data transfers for skew/drift checks, and a retrain policy (thresholds based on feedback volume and NDCG) show operational maturity.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `infra/terraform/modules/slo/`, `infra/terraform/modules/monitoring/`), `app/services/retrain_policy.py`

- **Secret management is widespread** – The high `env_secret` hit count (613) and references to Secret Manager, Workload Identity, and external-secrets-operator indicate that secrets are a critical and carefully managed concern.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md`, `evidence/08_config_env.md` (redacted secret references)

- **Infrastructure surface is broad** – 1620 infra_surface hits plus 602 high_risk_ops hits imply many automation scripts modify cloud resources (terraform, kubectl, gcloud). This raises operational risk and requires tight change control.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md`

- **Dependency injection pattern for GCP clients** – The `ContainerBuilder` and `InfraBuilder` classes conditionally resolve adapters (e.g., fetcher, publisher, scorer) based on configuration, making the system locally testable while supporting cloud-only services.  
  *Evidence_ref*: `evidence/03_symbols.md` (e.g., `app/container/infra.py`, `app/container/search.py`)

## uncertainty_notes

- **Parser limitations for dynamic symbols** – Symbols extracted heuristically may miss macros, dynamic classes, or decorator-registered routes. Rust macro expansions, Python import hooks, and decorated functions are not fully captured.  
  *Evidence_ref*: `evidence/99_scan_limitations.md`

- **Grep dependence** – Static signal hits rely on substring matching; no-hit does not prove absence. Domain-specific naming or synonyms may cause false negatives.  
  *Evidence_ref*: `evidence/99_scan_limitations.md`

- **Environment variable requiredness unknown** – The config/env inventory does not differentiate required vs. optional variables, nor default values. Usage context from code may clarify but is not fully provided.  
  *Evidence_ref*: `evidence/08_config_env.md` (final line: "required/optional は未確認")

- **Secrets redacted** – Many environment variable values, secret IDs, and resource names are redacted. This prevents full assessment of dependency paths and access patterns.  
  *Evidence_ref*: `evidence/08_config_env.md` (all values are `redacted (name/参照のみ)`)

- **Change signals are observations only** – The `30_static_signal_hits.md` cautions that static signal entries are not decisions; they only indicate that certain files have been recently modified. Interpretation requires review of actual changes.  
  *Evidence_ref*: `evidence/30_static_signal_hits.md` (Guardrail note)

- **symbol responsibility unpublished** – The scan did not assign responsibility or meaning to symbols; this investigation step is deferred to the Decision Catalog.  
  *Evidence_ref*: `evidence/99_scan_limitations.md` ("検出したシンボルの責務は未判定")

## judgment_value_added

- Raw inventory has been classified into draft inputs: observed signals, roles, and current implications.
- LLM enrichment, when present, adds meaning for each evidence item without changing observed evidence.
- This file does not approve an implementation choice or prescribe future work. It prevents raw scan output from being treated as a completed Decision Catalog.

## draft_inputs

- Draft must create `catalog_items` where each item pairs fact and meaning.
- Draft must not include advice, recommendations, next actions, validation plans, rollback plans, or change boundaries.
- Draft must cite evidence_ids for fact items and must not invent facts outside the Evidence Pack.

## required_llm_enrichment

- Assign role/current implication to evidence items.
- Keep risk language descriptive and current-state only.
- Put judgment-relevant uncertainty in descriptive current implications instead of a separate field.

## next_step

- Run `dcm draft <TARGET>` or `dcm llm draft <TARGET>` only after this investigated findings file exists.
