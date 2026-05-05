# AGENTS.md

## Purpose

Agent operating guide for this personal MLOps learning project. Use this file as the **Cursor / Codex-style project charter** for agents (parallel to [`CLAUDE.md`](CLAUDE.md), which is optimized for Claude Code). Prefer [`CLAUDE.md`](CLAUDE.md) for the fullest constraint text; use this file for quick routing and tool-equivalence below.

### Claude Code ↔ Cursor mapping (concept-level)

| Claude Code concept | Role | Cursor equivalent in this repo |
| --- | --- | --- |
| `CLAUDE.md` | Always-loaded charter, build/test, bans | [`CLAUDE.md`](CLAUDE.md) + this [`AGENTS.md`](AGENTS.md) |
| `.claude/rules/` | Path- or mode-specific rules | [`.cursor/rules/*.mdc`](.cursor/rules/) (this repo has no `.claude/rules/`; rules are split between `CLAUDE.md` and `.cursor/rules/`) |
| Subagents / custom agents | Specialized agent prompts | Cursor Agent / Cloud Agent; **reference prompts** (read-only handoff): [`.claude/agents/*.agent.md`](.claude/agents/) |
| Skills | Reusable procedures | Cursor **Agent Skills** (editor-level); repo sources: [`.claude/skills/`](.claude/skills/), [`.github/skills/`](.github/skills/) |
| Slash commands / commands | Manual bootstraps | [`.cursor/commands/`](.cursor/commands/) and [`.claude/commands/`](.claude/commands/) (keep text in sync when possible) |
| Hooks | Deterministic post-edit scripts | [`.claude/hooks/`](.claude/hooks/) (Claude Code). Cursor: optional Hooks or rely on CI / `make check` |
| MCP | External systems | Configured in Cursor **MCP** settings (per user/env) |
| Review rules | Reviewer policy, bug patterns | [`.cursor/rules/`](.cursor/rules/) + team review / Bugbot if enabled |

### Codex mapping (this repo)

| Need | Codex equivalent |
| --- | --- |
| Always-loaded repo charter | [`AGENTS.md`](AGENTS.md) |
| Deep constraint text / historical rationale | [`CLAUDE.md`](CLAUDE.md) |
| Repo-local Codex notes / handoff memos | [`.codex/README.md`](.codex/README.md), [`.codex/playbooks.md`](.codex/playbooks.md) |
| Claude hook behavior to emulate manually | [`.codex/playbooks.md`](.codex/playbooks.md) |

Important: Codex does **not** consume `.claude/hooks/` or `.claude/settings.json` directly. If a Claude Code workflow is still useful, document the intent in `AGENTS.md` / `.codex/*` and enforce it via normal repo commands (`make check-layers`, `make check`, targeted pytest, etc.).

### Tool surface mapping (where each concern lives)

| Concern | Claude Code | Cursor (this repo) |
| --- | --- | --- |
| Charter / "read first" | `CLAUDE.md` | `AGENTS.md` + `CLAUDE.md` |
| Fine-grained rules | `CLAUDE.md` sections + (optional) `.claude/rules/` | `.cursor/rules/*.mdc` |
| Agent role prompts | `.claude/agents/*.agent.md` | Same files as **documentation**; paste or @-reference in chat when simulating that role |
| Skills | `.claude/skills/<name>/SKILL.md` | Same paths; optional mirror in user Agent Skills |
| Commands | `.claude/commands/*.md` | `.cursor/commands/*.md` |

## Repo Charter

This is a personal technical learning project: 不動産ハイブリッド検索 + 継続改善 MLOps サイクル. Stack: **Cloud Composer (本線 orchestration) + Vertex AI Pipelines / Feature Store / Vector Search / Model Registry + GKE Deployment + KServe InferenceService + PMLE 統合技術**. Real-world reference architecture in design docs only: Elasticsearch + Redis 同義語辞書 + ME5 + Vertex AI Vector Search + LightGBM (the repo intentionally substitutes Meilisearch + Redis cache for learning-friendliness).

Primary navigation:

- [README.md](README.md)
- [CLAUDE.md](CLAUDE.md)
- [docs/README.md](docs/README.md)
- [docs/tasks/TASKS.md](docs/tasks/TASKS.md) — current sprint (read first)

## Non-Negotiable Constraints

- Keep the hybrid-search **5-element core** intact: **Meilisearch BM25 + multilingual-e5 + Vertex AI Vector Search + RRF + LightGBM LambdaRank**. Removal/replacement requires explicit user approval.
- **Vertex AI Feature Store (Feature Group / Feature View / Feature Online Store)** is mandatory (training-serving skew prevention). KServe references the Feature Online Store via Feature View opt-in.
- **Cloud Composer (Managed Airflow Gen 3)** is the canonical orchestrator with 3 DAGs (`daily_feature_refresh` / `retrain_orchestration` / `monitoring_validation`). Vertex `PipelineJobSchedule` must stay removed (no double-trigger). Cloud Scheduler / Eventarc / Cloud Function triggers remain only as smoke / manual / lightweight alternatives — never running the same retrain job through two paths.
- **Vertex Vector Search** is the production serving index for ME5 vector search. Canonical embedding history / metadata stays in BigQuery (data lake + serving index two-layer model).
- **Event schema common contract**: `search_events` / `search_impressions` / `user_actions` (3 tables) + `action_type` enum 8 values (app emit 5: `click` / `detail_view` / `favorite` / `request_button_click` / `request_complete`; synthetic-only 3: `inquiry_complete` / `contract` / `bounce`) + weighted relevance label (`click`=1, `detail_view`=2, `favorite`=3, `request_button_click`=4, `request_complete`=5, `inquiry_complete`=7, `contract`=10, `no_action`=0, `bounce`=0/-1). Synthetic injection writes `ranking_labels.label_source='synthetic_*'` from `definitions/labeling/synthetic_actions.yaml`. `ml/labeling/` must remain pure (no psycopg / google.cloud imports).
- ⚠️ **canonical death line (LightGBM wiring)**: `pipeline/training_job/main.py` must call `ml/data/loaders/ranker_repository.py` (BigQuery loader); without that wire-up, real `ranking_labels` never reach LightGBM training (current state: trainer uses `synthetic_ranking_frames`).
- Meilisearch is a learning-friendly substitute for Elasticsearch; swap requires explicit user approval.

Canonical references:

- [README.md](README.md)
- [CLAUDE.md](CLAUDE.md)
- [docs/architecture/01_仕様と設計.md](docs/architecture/01_仕様と設計.md)
- [docs/architecture/03_実装カタログ.md](docs/architecture/03_実装カタログ.md)
- [docs/runbook/05_運用.md](docs/runbook/05_運用.md)
- [docs/conventions/README.md](docs/conventions/README.md) — naming / placement / Make / Docker convention index

## Build & Test Commands

```bash
make doctor                    # verify prerequisite tools
make sync                      # uv sync (full workspace)
make help                      # list all targets

make check                     # ruff + ruff format --check + mypy strict + pytest
make check-layers              # AST-based Port-Adapter boundary check
make tf-validate               # terraform validate (offline)

make verify-local-app          # FastAPI boot + DI + API contract
make verify-local-ml           # ML / pipeline unit + smoke train
make verify-local-hybrid       # workflow contract + the above

make deploy-all                # 15-step deploy (tf-bootstrap → 2-stage apply → seed → meili-sync → composer-deploy-dags → deploy-api)
make run-all                   # 12-step canonical validation
make destroy-all               # no-prompt 4-stage teardown
```

## Documentation Rules

- Link to existing docs instead of duplicating long policy text.
- Authority order: `tasks/TASKS_ROADMAP.md > tasks/TASKS.md > 01_仕様と設計.md > README.md > CLAUDE.md`.
- For root-level doc updates, keep terminology synchronized with `docs/architecture/` content.

## Guardrails

- Do not perform broad refactors by default; keep changes scoped to the task at hand.
- The 5-element core, Composer × Vertex Pipelines hierarchy, and Event schema contract require explicit user approval to alter.
- Force-pushes to main, ADR creation, and replacement of Meilisearch with Elasticsearch require human judgment, not agent autonomy.

## Existing Chat Customizations

- Cursor rules: [`.cursor/rules/`](.cursor/rules/) (`study-gcp-mlops-core.mdc`, `python-fastapi-ml.mdc`, `terraform-gcp-mlops.mdc`)
- Cursor command: [`.cursor/commands/check-parity.md`](.cursor/commands/check-parity.md) (alias intent of [`.claude/commands/check-parity.md`](.claude/commands/check-parity.md))
- Claude Code agents: [`.claude/agents/`](.claude/agents/) (use as **prompt references** in Cursor)
- Claude Code skills: [`.claude/skills/`](.claude/skills/)
- Codex repo-local notes: [`.codex/`](.codex/)
- GitHub: [.github/agents/gcp-mlops-theme-research.agent.md](.github/agents/gcp-mlops-theme-research.agent.md)

Use them when tasks match their scope; otherwise follow this AGENTS guide and `CLAUDE.md`.
