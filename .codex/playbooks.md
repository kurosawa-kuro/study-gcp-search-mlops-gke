# Codex Playbooks

Small, explicit workflows that replace the useful intent of `.claude/hooks/*` when working with Codex.

## 1. Session Start

Claude Code used to show the sprint file automatically.

Codex equivalent:

```bash
head -50 docs/tasks/TASKS.md
```

Fallback when `docs/tasks/TASKS.md` does not exist:

```bash
head -50 docs/TASKS.md
```

## 2. After Port / Adapter Boundary Edits

Claude Code used to background-run `make check-layers` after edits in sensitive areas.

Sensitive areas:

- `app/services/`
- `app/composition_root.py`
- `app/api/`
- `app/domain/`
- `app/schemas/`
- `ml/*/ports/`
- `ml/*/adapters/`
- `pipeline/*/ports/`
- `pipeline/dags/`
- `scripts/ci/layers.py`

Codex equivalent:

```bash
make check-layers
```

## 3. Feature Parity Changes

When a ranker feature is added / removed / renamed, check the 6-file invariant:

```bash
rg -n "<feature_name>" \
  pipeline/data_job/dataform/features/property_features_daily.sqlx \
  ml/data/feature_engineering/ranker_features.py \
  ml/data/feature_engineering/schema.py \
  infra/terraform/modules/data/main.tf \
  infra/sql/monitoring/validate_feature_skew.sql \
  infra/terraform/modules/vertex/main.tf
```

## 4. Local-Only Safety

If the user says local-only, stay inside:

```bash
make verify-local-app
make verify-local-ml
make verify-local-hybrid
```

Avoid `deploy-all`, `run-all`, `destroy-all`, Terraform apply, and live GCP acceptance unless the user explicitly re-allows them.

## 5. Canonical Endpoint Drift Check

Public API:

- `/api/v1/search`
- `/api/v1/feedback`

Ops:

- `/ops/jobs/check-retrain`
- `/ops/model/info`
- `/ops/model/metrics`
- `/ops/model/data`

Useful grep:

```bash
rg -n '"/search"|"/feedback"|"/model/info"|"/model/metrics"|"/jobs/check-retrain"' app tests scripts
```

Review any remaining hits carefully; some may be legacy redirect tests, but new code should prefer canonical paths.
