# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済み実装ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)。

---

## 本 sprint scope (2026-05-09)

- 対象: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §1 #4 / #5 と Wave 5 / Wave 8 の残件
- **scope outside**: Wave 9 (独自ドメイン + HTTPS + DNS) — user 指示で本 sprint 除外

---

## 完成定義 (Definition of Done)

下記 1 項目が ✅ になれば本 sprint 完了。完了済 (T2 / T3 / T4 / T5) は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §7.3 へ移管済。

| ID | タスク | 完了条件 | 着手コマンド / 手順 |
|---|---|---|---|
| T1 ⚠️ | M-Wave5 live 検証通し | `make verify-live-acceptance` が PASS | step 10 (sync-elasticsearch) 完了後に着手。下記「2026-05-09 中断点」参照 |

⚠️ = canonical 必須項目。[`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) §0.1 ゴール劣化禁止対象。

---

## 2026-05-10 中断点 (翌セッション resume 用)

**cluster は destroy 完了 / clean state**:
- `terraform state list` 空 / GKE / Composer / KServe / Pub/Sub / Vertex Endpoint shell すべて削除
- 残置: tfstate bucket / API 有効化 / **VVS Index/Endpoint** (persistent design 通り)、コスト止血済

### 着手手順 (翌セッション)

1. **新コードで一発復活トライ** (推奨):
   ```bash
   make deploy-all
   ```
   今回反省を反映した修正により、以下が自動化されている:
   - tf-apply 冒頭の `recover_wif` idempotent hook (WIF 409 自動回復)
   - step 10 (`sync-elasticsearch`) 前の ES health wait (Phase=ApplyingChanges race 自動回避)
   - terraform_lock parser の ANSI escape 対応 (lock 残存時に `TERRAFORM_STATE_FORCE_UNLOCK=1` で自動 unlock + retry)

2. T1 `make verify-live-acceptance` 走行 → M-Wave5 ✅

3. cluster 残置を避けるなら最後に `make destroy-all` (新 step 分離で `--from-step` slicing 可能)

### 細かく進めたい場合

`uv run python -m scripts.setup.deploy_all --from-step <step> --to-step <step>` で 1 step ずつ。step 名一覧:

```
tf-bootstrap, tf-init, recover-wif, sync-dataform, tf-plan, tf-apply,
seed-lgbm-model, seed-test, apply-manifests, sync-elasticsearch,
backfill-vvs, trigger-fv-sync, overlay-configmap, composer-deploy-dags,
deploy-api
```

### 解消済みの並行課題 (2026-05-10)

| ID | 課題 | 解消 |
|---|---|---|
| C1 | `make sync-elasticsearch` Makefile target が env を引き渡していない | ✅ Makefile に `--project-id=$(PROJECT_ID)` + `--es-url` のフォールバック追加。contract test pin |
| C2 | `_run_sync_elasticsearch` 前に ES health wait がない | ✅ `scripts/infra/elasticsearch_wait.py` 新設、`_run_sync_elasticsearch` 冒頭で `wait_until_es_healthy()`。contract test pin |

### 残課題 (低優先、別 sprint)

| ID | 課題 | 詳細 |
|---|---|---|
| C3 | `verify-local-hybrid` の説明 (CLAUDE.md) と実装ズレ | CLAUDE.md は「`workflow contract + verify-local-app + verify-local-ml`」と説明しているが、実走ログには workflow contract が含まれない。Makefile の verify-local-hybrid target を確認して説明 or 実装の整合化 |

---

## 次 sprint (本 sprint 外)

- **M-Wave8.5 Phase 概念完全撤廃**: 現 sprint で canonical wording として残置した「Phase 7 で本実装、後方派生で Phase 6 へ引き算」(01 §3 / workflow contract test 15+ / runbook 数十箇所) を固有名 (canonical / Composer なし派生) へ完全置換。完了条件: `grep -rE "Phase [0-9]" docs/ tests/integration/workflow/` が **0 件**。詳細は [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §2 Wave 8.5
- **M-Wave8.6 orchestrator ドメイン分離 Phase 2/3**: Phase 1 (step 分離 + tf_apply.py 切り出し + destroy_all 対称化) は 2026-05-09 完了 (03_実装カタログ §7.3)。Phase 2 (`scripts/infra/*` → `scripts/domain/{gcp,k8s,terraform,data}/`) / Phase 3 (subprocess wrapper を `scripts/adapters/`) が残件。詳細は [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §2 Wave 8.6

---

## 参照

- 完了済み実装スナップショット + マイルストーン履歴: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- Wave / 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証ゲート定義 (V1-V6): [`../runbook/04_検証.md`](../runbook/04_検証.md)
- PDCA / 運用手順: [`../runbook/05_運用.md`](../runbook/05_運用.md)
