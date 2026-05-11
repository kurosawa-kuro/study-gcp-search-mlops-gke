# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済の実装ログ + マイルストーン履歴 + incident memo は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 / §7.3 / §7.4 を正本。

---

## sprint 状態 (2026-05-11 時点)

**完了**:
- **M-Wave9 全 Step 完了 (独自ドメイン + HTTPS + DNS、Web 公開基盤)**: `make deploy-all` 15/15 完走 (~72 min) → `gcp-search-mlops-gke.dev` の Certificate Manager cert `managed.state=ACTIVE` / `dig +short` = 静的グローバル IP / `make ops-search TARGET=gcp` (= `https://gcp-search-mlops-gke.dev/api/v1/search`) HTTPS 200 / `curl -I` HTTP/2 + Google Trust Services cert / `make ops-search-components` `lexical=4 semantic=3 rerank=5` を確認。M-Wave9 は backlog から外れた
- **`make run-all-core` 完走確認**: 16/16 step PASS、9m16s。`label-build` が `ranking_labels` 61 件 materialize → `ops-train-now`/`ops-train-wait` で Vertex pipeline `state=SUCCEEDED` → `ops-accuracy-report` `ndcg=hit_rate=mrr=1.0`（G5 PASS）
- **deploy-path regression 5 件修正** (M-Wave8.6 reorg が deploy 専用パスに残した欠陥、`make check` をすり抜け): `tf_plan.py` の `terraform_var_args()` 漏れ → step 5 fail / stdlib `subprocess.run(..., capture=True)` 3 箇所 (`state_recovery` ×2 + `vertex_feature_store_wait`) → step 6 `TypeError` / `feature_view_sync.py`・`state_recovery.py::main` の `parents[2]` ずれ → step 12 `terraform output -json failed`。AST-scan guard test 2 種追加（詳細: [`../architecture/03_実装カタログ.md §7.4`](../architecture/03_実装カタログ.md)）
- **step-timing 計測の仕組み**: 共有モジュール `scripts/lib/step_timing.py` で `deploy-all` / `destroy-all` / `run-all` の各 step wall time を `logs/step_timings.csv`（gitignore、`flow` カラム付き）に記録、起動時に過去 run の median から **ETA + 重い step トップ3** を表示。`run-all-core` は bash recipe → Python orchestrator `scripts/ops/run_all.py` に変換（同時に step 順を `ops-label-seed → label-build → ops-train-now` に修正 — 旧順は空 `ranking_labels` で `train-reranker` crash していた）。`make check` 840 passed / 2 skipped
- M-Wave5 (継続改善サイクル MVP) PASS、verify-live-acceptance 22.68s
- M-Wave8.5 (Phase 概念完全撤廃 — docs/ + tests/integration/workflow/ 範囲) 達成
- M-Wave8.6 Phase 1+2+3 + 後段 caller migration 完了 (orchestrator ドメイン分離 / adapters 構造 / `subprocess.run([cli, ...])` → `cli_run(...)` を 0 件まで削減)
  - 後処理: adapter 移行漏れ 3 件修正 (`tf_bootstrap` / `tf_init` の `gcloud_run(stdout=...)`、`slo_status` の `terraform_run(cwd=/text=/stdout=)`) + `_common.run` の `capture=True` を stdout/stderr 両捕捉に統一 (`subprocess.run(capture_output=True)` 相当 — `destroy_check` 等の `.stderr` 参照が空になっていた regression も同時解消)
- M-Wave7 Makefile 本格整理 (Phase Support Matrix 撤去 / `mk/base.mk` 削除 / `deploy-all-direct` + `verify-all` legacy alias 撤去 / `destroy-phase7-learning` → `destroy-coast-down` rename / `phase7-ml-base:local` → `mlops-ml-base:local` / `.SHELLFLAGS pipefail` 追加)
- GCP リソース ID rename: `phase7-synonym` → `mlops-synonym` (Memorystore + Secret + ExternalSecret)
- EventWriter Pub/Sub 統一 (canonical 3-table emit silent gap 解消): `PubSubEventWriter` + `search-events` / `search-impressions` / `user-actions` の 3 topic + 3 BQ Subscription + 3 IAM、`CloudLoggingEventWriter` は bootstrap fallback
- **M-Wave9 Step 1-5** (公開ドメイン): `gcp-search-mlops-gke.dev` 購入 + Cloud DNS zone `gcp-search-mlops-gke-dev` 作成 (Step 1-2) + `infra/terraform/modules/dns/` 新設 (予約グローバル IP / Certificate Manager DNS-01 / certmap / apex A record) + gateway.yaml certmap annotation + static IP pin + hostname 差替え + `env/config/setting.yaml` に `public_domain` / `dns_zone_name` 追加 + `_common.terraform_var_args()` を canonical 既定にリファクタ + `resolve_api_target(TARGET=gcp)` を公開ドメイン優先に二段化 (Step 3-5)。`make check` 818 passed、`make tf-validate` / `tf-fmt` PASS
- `.claude` / `.cursor` / `.github` / `.codex` の Phase 残骸 modernize (`phase-subtraction-derivator` → `derivation-by-subtraction-reviewer` / `phase-doc-sync` → `doc-sync` / `.cursor/rules/*` の Phase model 撤去 等)
- C4 Makefile `python -u -m` 統一 (line buffer 強制、bg-pipe 罠予防) / PMLE 学習 doc 8 章新設

cluster は **稼働中** (`make deploy-all` + `make run-all-core` 成功直後、`destroy-all` 未実施 — コスト発生中)。`make destroy-all` で永続 VVS Index/Endpoint のみ残してゼロに戻せる。次セッションは clean state から `make deploy-all` 一発で復活可能。

## 残課題 (優先度順)

| # | 内容 | コスト | 状態 |
|---|---|---|---|
| 1 | M-Wave8.7 ES production 化 (HTTPS + password auth、Step 7-1〜7-5) | 半 sprint | ⏸ M-Wave9 完了済 → 着手可 |
| 2 | `infra/` 配下の Phase 残骸 ~25 箇所 scrub (Terraform module コメント + manifest コメント、M-Wave8.5 が docs/ + tests/ のみだった分。コード影響なし、全てコメント) | 軽 | ⏳ 着手可 |
| 3 | doc 同期 (`docs/runbook/04_検証.md` / `05_運用.md` / `docs/conventions/Makefile規約.md` の `run-all-core` step 順記述を新 16-step orchestrator (`scripts/ops/run_all.py`) に追従、`make run-all-core` を `uv run python -u -m scripts.ops.run_all` 経由に表記更新、step-timing CSV の運用メモ追記) | 軽 | ⏳ 着手可 |
| 4 | (任意) Helm provider 3.x 移行 (`versions.tf` `~> 3.0` + `kubernetes { }` → `kubernetes = { }`) | 軽 | ⏸ |

具体手順は [`TASKS_ROADMAP.md §2 Wave 8.7`](TASKS_ROADMAP.md#2-残-wave-詳細) に gcloud / kubectl / file edit / 検証コマンド単位で展開済。

## 参照

- 完了済: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証 / PDCA: [`../runbook/04_検証.md`](../runbook/04_検証.md) / [`../runbook/05_運用.md`](../runbook/05_運用.md)
- troubleshooting: [`../troubleshooting/`](../troubleshooting/)
- PMLE 学習 doc: [`../pmle-learning-notes.md`](../pmle-learning-notes.md)
