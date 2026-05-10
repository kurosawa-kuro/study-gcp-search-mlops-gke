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

## 2026-05-09 中断点 (翌日 resume 用)

**cluster は live のまま** (mlops-dev-a / GKE 5 nodes / Composer / VVS / ES on GKE)。コスト累積中。翌日続けるか destroy-all で止めるかは下記で判断。

### 完了済 step (個別 target で逐次実行)
- step 1 `tf-bootstrap` ✅ / 2 `tf-init` ✅ / 3 `recover-wif` ✅ / 4 `sync-dataform-config` ✅ / 5 `tf-plan` ✅ (188 add)
- step 6 `tf-apply` ✅ (1 回目失敗 → recover-wif → 31 分で完走)
- step 7 `seed-lgbm-model` ✅ / 8 `seed-test` ✅ / 9 `apply-manifests` ✅

### 中断点
- **step 10 `sync-elasticsearch`**: 失敗 (ES `HEALTH=unknown PHASE=ApplyingChanges` で API endpoint 未起動)。中断時 ES wait の bg job kill 済。

### 翌日の着手手順 (deploy-all を使わず細かく)
1. cluster 生存確認: `kubectl get nodes` / `kubectl -n search get elasticsearch`
2. ES が `green`/`yellow` になるまで待機 (起動から 5-10 分で到達のはず):
   ```
   until h=$(kubectl -n search get elasticsearch elasticsearch -o jsonpath='{.status.health}'); [ "$h" = "green" ] || [ "$h" = "yellow" ]; do sleep 15; done
   ```
3. `uv run python -m scripts.setup.deploy_all --from-step sync-elasticsearch --to-step sync-elasticsearch`
4. step 11 `backfill-vvs` / 12 `trigger-fv-sync` / 13 `overlay-configmap` / 14 `composer-deploy-dags` / 15 `deploy-api` を `--from-step / --to-step` で 1 つずつ
5. T1 `make verify-live-acceptance` 走行 → M-Wave5 ✅
6. cluster 残置の場合は最後に `make destroy-all` (= 新 step 分離で `--from-step` slicing 可能)

### 並行課題 (本 sprint 外、低優先)

| ID | 課題 | 詳細 |
|---|---|---|
| C1 | `make sync-elasticsearch` Makefile target が env を引き渡していない | 個別 `make sync-elasticsearch` で実行すると `ELASTICSEARCH_URL is empty` で fail。deploy_all 経由なら OK。Makefile 側で `ELASTICSEARCH_URL` / `--es-url` を明示する修正が必要。Wave 0 / Wave 7 の延長 |
| C2 | `_run_sync_elasticsearch` 前に ES health wait がない | step 10 が ES 起動完了より早く走ると `Server disconnected` で fail。`_run_sync_elasticsearch` 冒頭で `kubectl wait` または `cluster_health` polling を組み込むべき |
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
