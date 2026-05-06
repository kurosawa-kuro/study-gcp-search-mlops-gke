# TASKS — current sprint dashboard

権威順位は [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) を参照。ここは **短周期の作業メモ・検証ログの置き場**。

---

## Latest session (2026-05-06)

**目的**: ML→APP の順で動作検証（ローカル → Cloud）。コード変更は検証でギャップが出た場合のみ。

**ROADMAP**: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) §5 に `M-RunbookLocal`（ローカルゲート到達）を追記済み。短周期のコマンド表は本書が canonical。

### 進捗更新（2026-05-06 14:34 JST）

- **コーディング済み（検証前）**:
  - Meilisearch 撤去（Terraform / scripts / docs の主要導線）
  - Elasticsearch workflow contract 追加
  - runbook / README / 実装カタログの Elasticsearch canonical 追従
- **これから検証**:
  - `make check`
  - 必要に応じて live 側 (`make deploy-all` → `make run-all`)

### ローカル — 成功

| Step | Command | Result |
|------|---------|--------|
| ML | `make verify-local-ml` | PASS（pytest 97 passed, `train-smoke` 完了） |
| APP | `make verify-local-app` | PASS（check-layers OK, pytest 207 passed） |
| L2 | `DOCKER_BUILDKIT=1 docker build -f infra/run/services/search_api/Dockerfile -t local-test/search-api:dev .` | PASS |
| Image size | `docker image inspect ... '{{.Size}}'` | ~709MB |
| L3 import | `docker run ... -c "from app.main import app; ..."` | PASS |
| L4 `/livez` | `ENABLE_SEARCH=false` コンテナ + GET `/livez` | PASS（200, `{"status":"ok"}`） |

**テスト追加**: 今回の実行分では不整合なし（未改修）。

### Cloud — 逐次復旧（2026-05-06 16:45 JST）

| Step | Result | メモ |
|------|--------|------|
| Terraform stage1 (`module.iam/data/vector_search/vertex/gke/messaging/monitoring/slo/composer`) | PASS | `oncall_email` 対話入力待ちは `-var` 明示で解消。既存 Composer は `terraform import` 後に apply 成功 |
| Terraform `-target=module.kserve` | PASS | `search` / `kserve-inference` namespace と CRD（KServe/ExternalSecret）を作成 |
| `make apply-manifests` | PASS | 先行失敗（namespace/CRD不足）は解消 |
| `make deploy-kserve-images` | PASS | encoder/reranker の Cloud Build 成功 + patch 成功 |
| `make seed-lgbm-model` | PASS | `gs://mlops-dev-a-models/lgbm/latest/model.bst` を生成・配置 |
| `make deploy-kserve-models` | PASS | `property-reranker` Ready 化（初回は storageUri 実体なしで FailedToLoad） |
| `uv run python -m scripts.deploy.configmap_overlay` | PASS | `ELASTICSEARCH_URL` を ConfigMap に注入 |
| `make deploy-api` + `make ops-livez` | PASS | rollout 成功、`{"status":"ok"}` |
| `ops-search-components` | PASS | `lexical=4 semantic=3 rerank=5`（all non-zero） |
| `ops-vertex-vector-search-smoke` | PASS | 5 neighbors 返却 |
| `ops-vertex-feature-group` | PASS | `property_id='p001'` で 7 features 取得 |
| `ops-accuracy-report` | **FAIL (gate未達)** | `ndcg_at_10=0.75`（target 1.0） |

**次アクション（進行中）**: `seed-test → sync_elasticsearch → ops-train-now → ops-train-wait → ops-accuracy-report` を 1 ステップずつ実行し、`ndcg_at_10=1.0` 到達まで詰める。

**いまの優先**: Cloud 精度ゲートの達成（`ndcg_at_10=1.0`）。

---

## メモ（未整理）

- **コード ↔ 仕様の機械的ロック**: `tests/integration/parity/test_codebase_invariants.py` が runbook §2 **L1''**（W2-8 残骸）と **Elasticsearch-only lexical** を `app` / manifests / `Makefile` / `pyproject` で CI 検証。補足は [`tests/integration/parity/README.md`](../../tests/integration/parity/README.md)。
- **ローカル優先ゲート**: `make verify-local-parity`（parity のみ）→ `make verify-local-hybrid` がその後に app/ML を続ける。Phase 7 本線は GCP/cluster 依存のため **ローカル完結は runbook §2 の範囲**（`04_検証.md` §2.1 / §3）。
- **全体ゲート**: `make check`（フルテスト）+ [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) Findings。
