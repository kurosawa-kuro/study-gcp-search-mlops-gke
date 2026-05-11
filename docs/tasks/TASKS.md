# TASKS — current sprint

権威順位: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md) > 本書 > [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)。
完了済の実装ログ + マイルストーン履歴 + incident memo は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 / §7.3 / §7.4 を正本。

---

## sprint 状態 (2026-05-11 時点)

**完了済の検証・実装の詳細・証跡は本書に積まない** — [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) の §6 直近完了ログ / §7.3 マイルストーン履歴 / §7.4 incident memo を正本とする。本書は「現在の目的 / 残課題 / 完了条件」だけを薄く保つ。

直近の到達点 (1 行ずつ、詳細は 03):

- **M-Wave9 公開ドメイン + HTTPS + DNS — 全 Step (1-6) 完了 (2026-05-11)**。`https://gcp-search-mlops-gke.dev` で HTTPS serving 成立 (cert `managed.state=ACTIVE` / `make ops-search TARGET=gcp` 200 / `make run-all-core` 16/16 完走、`ndcg=hit_rate=mrr=1.0`)。backlog から外れた
- step-timing 計測 + `run-all-core` orchestrator 化 (2026-05-11) — `logs/step_timings.csv` への per-step 記録 + 起動時 ETA、`run-all-core` を `scripts/ops/run_all.py` 化 (step 順も `ops-label-seed → label-build → ops-train-now` に修正)
- 完了済 milestone (M-Wave5 継続改善サイクル MVP / M-Wave6 ES 移行 / M-Wave7 Makefile canonical 化 / M-Wave8.5 Phase 撤廃 / M-Wave8.6 scripts reorg + adapters / EventWriter Pub/Sub 統一 / GCP リソース ID rename / PMLE 学習 doc / 等) の一覧と証跡は 03 §7.3。

cluster は **稼働中** (`make deploy-all` + `make run-all-core` 成功直後、`destroy-all` 未実施 — コスト発生中)。`make destroy-all` で永続 VVS Index/Endpoint のみ残してゼロに戻せる。

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
