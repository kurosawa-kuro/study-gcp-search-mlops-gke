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

cluster: `make destroy-all` で永続 VVS Index/Endpoint のみ残してゼロに戻せる（PDCA loop。`deploy-all` で復活、`destroy-all` で止血）。

## 残課題 (優先度順)

| # | 内容 | コスト | 状態 |
|---|---|---|---|
| 1 | (任意) Helm provider 3.x 移行 (`versions.tf` `~> 3.0` + `provider "helm" { kubernetes { … } }` → `kubernetes = { … }` 属性記法)。**放置で致命的問題なし**（provider 2.x で現状動作。helm 2.17 が最終 = メンテ終了、将来 terraform / 他 provider を上げる時の足かせ回避が唯一の動機） | 軽 | ⏸ 低優先 / スキップ可 |

**次のアクティブ作業候補**（詳細はユーザ側で展開）: Vector Search 3 層永続化 PR（`vector_search` stack 分離）/ `ml/` ディレクトリ再編。

**parked / 完了** (2026-05-11):
- ES production 化 (旧 M-Wave8.7、Step 7-1〜7-5) → active backlog から外し parked。学習リポジトリは production hardening を追わない判断。手順 + 判断記録 + 破綻条件は [`../backlog/production-hardening.md`](../backlog/production-hardening.md)。contract test `test_es_manifest_pins_http_and_anonymous_auth` は現行 pin (HTTP + anonymous superuser = 学習用) のまま残る
- `infra/` Phase 残骸 scrub（~120 occurrence、コメント / description のみ → 固有名）: 完了
- `run-all-core` step 順 / step-timing CSV の doc 同期（`04_検証.md` / `05_運用.md` / `Makefile規約.md`）: 完了

## 参照

- 完了済: [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)
- 長期 backlog / 不変ルール: [`TASKS_ROADMAP.md`](TASKS_ROADMAP.md)
- canonical 仕様: [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- 検証 / PDCA: [`../runbook/04_検証.md`](../runbook/04_検証.md) / [`../runbook/05_運用.md`](../runbook/05_運用.md)
- troubleshooting: [`../troubleshooting/`](../troubleshooting/)
- PMLE 学習 doc: [`../pmle-learning-notes.md`](../pmle-learning-notes.md)
