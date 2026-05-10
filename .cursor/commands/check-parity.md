---
description: "Run a feature parity check for the 6-file invariant (ranker features)."
argument-hint: "<feature-name> | <PR#> | <commit-range> | (empty for working-tree changes)"
---

# /check-parity (Cursor)

ranker / feature column を変更する change set で **6 ファイル parity invariant** を破っていないかを検査する。

**Invariant (6 files, same change set):**

1. `pipeline/data_job/dataform/features/property_features_daily.sqlx`
2. `ml/data/feature_engineering/ranker_features.py` → `build_ranker_features`
3. `ml/data/feature_engineering/schema.py` → `FEATURE_COLS_RANKER`
4. `infra/terraform/modules/data/main.tf` → `ranking_log.features` RECORD
5. `infra/sql/monitoring/validate_feature_skew.sql` → UNPIVOT
6. `infra/terraform/modules/vertex/main.tf` → `google_vertex_ai_feature_group_feature`

**Instruction to the agent**

Verify the 6-file feature parity invariant for: **$ARGUMENTS**

- `$ARGUMENTS` が空: working-tree changes (`git diff --name-only HEAD` または `main..HEAD`) を対象に。
- feature column 名らしき場合: その名前を 6 site 全てで grep。
- commit range (例 `main..HEAD`) の場合: `git diff --name-only` で取得。

Output: 6 site の table (TOUCHED / NOT TOUCHED / N/A) + **PASS** / **FAIL** + FAIL の場合は依存順に missing edits を列挙。

**Reference:** [`.claude/agents/feature-parity-checker.agent.md`](../../.claude/agents/feature-parity-checker.agent.md), [`CLAUDE.md`](../../CLAUDE.md) "Feature parity invariant"。
