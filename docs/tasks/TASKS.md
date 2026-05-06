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

### Cloud — **中止**（実装優先のため中断）

| Step | Result | メモ |
|------|--------|------|
| `make deploy-api`（初回） | FAIL | GKE `hybrid-search` 未存在（404） |
| `make deploy-all` | **ABORT**（SIGINT） | **step 6 `tf-apply` 中**に `KeyboardInterrupt`。ログ: `make ... Error 130`。Terraform 論理エラーではなく中断。途中適用分は GCP に残る。 |
| `make deploy-api`（再試行） | PARTIAL | Cloud Build SUCCESS → rollout で FAIL（当時 `namespace search` 未作成） |
| `deploy_all --from-step 12` | FAIL | 単独実行は namespace / CRD 未準備のため不可だった |

**再開するとき**: 状態確認後に `make deploy-all` をやり直す（冪等）。異常時は runbook / `state_recovery`。[`04_検証.md` §3](../runbook/04_検証.md)、[`05_運用.md` §1.6](../runbook/05_運用.md)。

**いまの優先**: **ローカル実装を進める**。Cloud 検証は別セッション。

---

## メモ（未整理）

- **コード ↔ 仕様の機械的ロック**: `tests/integration/parity/test_codebase_invariants.py` が runbook §2 **L1''**（W2-8 残骸）と **Elasticsearch-only lexical** を `app` / manifests / `Makefile` / `pyproject` で CI 検証。補足は [`tests/integration/parity/README.md`](../../tests/integration/parity/README.md)。
- **ローカル優先ゲート**: `make verify-local-parity`（parity のみ）→ `make verify-local-hybrid` がその後に app/ML を続ける。Phase 7 本線は GCP/cluster 依存のため **ローカル完結は runbook §2 の範囲**（`04_検証.md` §2.1 / §3）。
- **全体ゲート**: `make check`（フルテスト）+ [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) Findings。
