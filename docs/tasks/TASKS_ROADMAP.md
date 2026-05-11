# TASKS_ROADMAP

不動産ハイブリッド検索 + 継続改善 MLOps サイクルの **長期 backlog + 不変ルール + 残 Wave の母艦**。

権威順位: `TASKS_ROADMAP > TASKS > 01_仕様と設計 > README > CLAUDE`

完了済の実装ログ / マイルストーン履歴 / incident memo は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 (直近完了ログ) / §7.3 (マイルストーン履歴) / §7.4 (incident memo) を正本とする。本書は **未完了 / 残課題 / 不変ルール** のみ残す。

---

## §0. プロジェクト方針

### §0.1 ピボット完了 + Phase 概念完全撤廃 (M-Wave8.5、2026-05-10)

教育用 Phase 1〜7 形式は廃止、個人技術学習プロジェクトに pivot。`Phase [0-9]` キャピタル P 表記は docs / tests から完全撤去。

例外:
- ADR (`docs/decisions/`) は historical record として `Phase X` 表記を残置 (retroactive note は ADR README に明記)
- e2e test ファイル名 (`tests/e2e/test_phase7_*.py` / `live_acceptance_checks.py::test_phase7_*`) は historical fixture として残置 (rename すると fixture と手元の運用ログ参照が drift する)
- M-Wave マイルストーンの Phase 1/2/3 (M-Wave8.6 Phase 1/2/3 等) は milestone 段階の固有名 = 撤廃対象外
- GCP リソース ID は **2026-05-10 rename 済**: `phase7-synonym` → `mlops-synonym` (Memorystore + Secret + ExternalSecret); Make target `destroy-phase7-learning` → `destroy-coast-down`; Docker tag `phase7-ml-base:local` → `mlops-ml-base:local`

### §0.2 仕様の大本命 (正解データ + 継続改善サイクル)

行動ログ → 正解データ → 再学習 → 評価 → deployment gate → KServe 反映 を 1 本の継続改善サイクルとして実装。アプリ側 (EventWriter Port) とモデル側 (`pipeline/training_job/main.py` の Repository 配線) の両方で正解データ対応。**M-Wave5 で 2026-05-10 完了**。

### §0.3 検索基盤 (Elasticsearch on GKE)

Meilisearch を廃止、GKE 上で Elasticsearch (ECK) を稼働。Elastic Cloud は不採用。**M-Wave6 で完了**。production 化 (HTTPS + password auth) は **active backlog から外し parked** — 学習リポジトリは production hardening を追わない判断 (2026-05-11)。手順 + 判断記録 + 破綻条件は [`../backlog/production-hardening.md`](../backlog/production-hardening.md)。自己拘束として contract test `test_es_manifest_pins_http_and_anonymous_auth` が現行の HTTP + anonymous superuser (学習用 (a') 解) を pin したまま残る。

### §0.4 公開ドメイン (M-Wave9、2026-05-11 — **全 Step 完了**)

- ドメイン: **`gcp-search-mlops-gke.dev`** (Cloud Domains で購入。`.dev` TLD = Google が運用、**HSTS preload 強制 → HTTPS 必須** — HTTP-only でブラウザ到達不可、`curl` は HTTP でも可)
- Cloud DNS public zone: **`gcp-search-mlops-gke-dev`** (DNS 名 `gcp-search-mlops-gke.dev.`、DNSSEC on、ゾーンタイプ 公開)。**console で手動作成済** — Terraform 側は `data "google_dns_managed_zone"` で参照 (zone 自体は import せず管理外、record-set のみ Terraform 管理)
- GKE Gateway TLS は **Certificate Manager** 経由 (DNS-01 authorization + certmap annotation)。旧 self-signed Secret (`kserve/tls_dev.tf`) は `enable_self_signed_tls=false` で無効化、`api_insecure_tls` も解除
- ✅ **2026-05-11 全 Step (1-6) 完了** — deploy + cert ACTIVE + `make ops-search TARGET=gcp` 200 確認済。実装手順 + 検証証跡は [`../architecture/03_実装カタログ.md §6 / §7.3 / §7.4`](../architecture/03_実装カタログ.md)

---

## §1. 残課題 (current backlog)

| # | 残 | 関連 | 状態 |
|---|---|---|---|
| 1 | (任意) Helm provider 3.x 移行 — `versions.tf` `~> 3.0` + `provider "helm" { kubernetes { … } }` → `kubernetes = { … }` 属性記法 + `terraform init -upgrade` + `tf-validate` / `deploy-all` で回帰確認。**放置で致命的問題は無い** (provider 2.x で現状動作。helm 2.17 が最終でメンテ終了 = security fix 来ず、将来 terraform 本体 / 他 provider を上げる時の依存解決の足かせになりうる、というのが唯一の動機) | `versions.tf` (dev + kserve module) | ⏸ 低優先 / スキップ可 |

**次のアクティブ作業候補** (詳細はユーザ側で展開): Vector Search 3 層永続化 PR (`vector_search` stack 分離) / `ml/` ディレクトリ再編。

**parked / 完了**:
- ES production 化 (旧 M-Wave8.7、Step 7-1〜7-5): active backlog から外し parked — 学習リポジトリは production hardening を追わない判断 (2026-05-11)。手順 + 判断記録 + 破綻条件 → [`../backlog/production-hardening.md`](../backlog/production-hardening.md)
- `infra/` Phase 残骸 scrub (~120 occurrence、コメント / description のみ → 固有名へ): **2026-05-11 完了**
- `run-all-core` step 順 / step-timing CSV の doc 同期 (`04_検証.md` / `05_運用.md` / `Makefile規約.md`): **2026-05-11 完了**

完了済 Wave (0/1/2/3/4/5/6/7/8 / M-Pivot / M-RunbookLocal / M-Wave8.5 / M-Wave8.6 Phase 1-3 + 後段 caller migration + adapter 移行漏れ後処理 / Step.precondition framework / C4 Makefile python -u / PMLE doc / GCP ID rename `phase7-*` → `mlops-*` / `destroy-coast-down` / EventWriter Pub/Sub 統一 / **M-Wave9 公開ドメイン 全 Step (1-6)** / step-timing 計測 + run-all-core orchestrator 化 / infra Phase scrub) は [03_実装カタログ §7.3](../architecture/03_実装カタログ.md) を正本。

---

## §2. 残 Wave 詳細

### Wave 9 — Web 公開基盤 (独自ドメイン + HTTPS + DNS) — ✅ 全 Step (1-6) 完了 (2026-05-11)

`https://gcp-search-mlops-gke.dev` (Cloud Domains + Cloud DNS public zone `gcp-search-mlops-gke-dev` + `infra/terraform/modules/dns/` の予約グローバル IP / Certificate Manager DNS-01 / certmap / apex A record + gateway.yaml の certmap annotation + static IP pin + `_common.resolve_api_target` 公開ドメイン化) を実装し、deploy + 疎通検証 (cert `managed.state=ACTIVE` / `make ops-search TARGET=gcp` 200 / `make run-all-core` 16/16) まで完了。**Step 1-6 のコマンド単位手順 + 検証証跡 + deploy 前置きで同時修正した deploy-path regression 5 件 + run-all-core step 順バグ は [`../architecture/03_実装カタログ.md §6 / §7.3 / §7.4`](../architecture/03_実装カタログ.md) を正本とする**（本書 §2 は未完了 Wave のみ残す方針 — 完了 Wave の詳細は積まない）。

---

### ES production 化 (HTTPS + password auth) — active backlog から外し parked (2026-05-11)

学習リポジトリは production hardening を追わない判断 (理由: PMLE 範囲外 / 実務転用時の差分は検索品質・特徴量・ランキング学習側 / ECK reconcile stall 再現リスクが学習価値に見合わない / 「評価が運用に先行する」順序原則)。手順 (Step 7-1〜7-5) + 判断記録 + 破綻条件 (portfolio 外部公開 / 実務クラスタ転用 / 第三者ワークロード同居 / PMLE 範囲入り) は [`../backlog/production-hardening.md`](../backlog/production-hardening.md) を正本。自己拘束: contract test `test_es_manifest_pins_http_and_anonymous_auth` を現行の HTTP + anonymous superuser (学習用 (a') 解) のまま残し、その反転 = production 化に踏み切る宣言とする。

---

## §3. 不変ルール / 非負制約

### §3.1 ⛔ ゴール劣化禁止

「本線」「必須」「canonical」「不変」と書かれた要件 (中核 5 要素 / Composer = 上位 orchestrator / 本線 retrain DAG / Feature View 経由 fetch / LightGBM 接続死守ライン) を **未達のまま「完了」「OK」と扱うのは禁止**。

禁止する hedging:
- 「深追いは別 sprint」「現状で X 完了とみなし次へ」「Stage X.Y 未解決のまま完了扱い」
- 「task SUCCEEDED は別 sprint」「live verify は別 session」「明日以降」「後追い」
- 判断 A/B が並列に書かれている場合、勝手に A を選んで B を別 sprint へ送る (User 明示確認なし)

正しい扱い:
1. 未達は ⚠️ マーカー付きで「**canonical 未達 (= ゴール劣化)、追加 sprint 必須**」と明示
2. 必須項目と機能影響低の項目を **明確に区別**
3. 違反が生じる選択肢は ~~取り消し線~~ で不採用宣言

### §3.2 中核 5 要素

**Elasticsearch BM25 + multilingual-e5 + Vertex AI Vector Search + RRF + LightGBM LambdaRank**。削除・置換・無効化は明示的な user 合意がない限り実施しない。

### §3.3 LightGBM 接続死守ライン

`pipeline/training_job/main.py` から `ml/data/loaders/ranker_repository.py` (BigQuery loader) を呼ぶ配線を維持、synthetic-only 学習へ退行禁止。

### §3.4 Composer × Vertex Pipelines 上下関係

Composer = 上位 orchestrator、Vertex Pipelines = 下位 ML executor。`train/evaluate/register` を Composer 側に書かない (カニバリ禁止)。Vertex `PipelineJobSchedule` は併存禁止。Cloud Scheduler / Eventarc / Cloud Function は smoke / manual のみ。

### §3.5 incident postmortem は contract test 化

過去 incident は `tests/integration/workflow/` の contract test として固定化済 (15 件以上)。新 incident も同パターンで固定化。詳細: [03_実装カタログ §7.4](../architecture/03_実装カタログ.md)。

---

## §4. リスクと回避

| リスク | 回避 |
|---|---|
| Wave の並行実施で API 境界が複数版混在 | Wave 1 (API 4 軸) 完了済 |
| LightGBM 接続死守ラインを「Wave 5 で代替」と勘違いし飛ばす | §3.3 死守ライン明記 |
| ES 移行で同義語辞書 (`SynonymExpanderPort`) を破壊 | Redis 経路は維持、adapter 差し替えのみ |
| Wave 7 (Makefile 整理) を Wave 1-6 と同時に走らせる | Wave 1-6 完了後に着手 (前提達成済) |
| deployed_index 残置による VVS 課金事故 (1 replica = ¥1,460/日) | `make destroy-all` で能動 undeploy + Cloud Scheduler 自動 undeploy (backlog) + Billing Budget Alert (backlog) |

### §4.9 VVS 永続化 lessons learned

2026-05-03 incident で `Instance cannot be destroyed` が発生し `prevent_destroy` 設計が teardown と衝突。以後は **`prevent_destroy` 不採用、state rm + GCP 残置 pattern** を採用。

- `destroy-all` で永続化したい VVS リソースは `state rm` で tfstate から外す
- 次回 `deploy-all` では `terraform import` で state 復帰
- `state-recover` runbook と対で扱う

将来 backlog: Stack 分離、Cloud Scheduler 自動 undeploy、Billing Alert、health check 強化。

---

## §5. 残マイルストーン

| ID | 内容 | 状態 |
|---|---|---|
| M-Wave9 | 独自ドメイン + HTTPS + DNS — 全 Step (1-6) | ✅ 完了 2026-05-11 |
| step-timing 計測 + run-all-core orchestrator 化 | per-step CSV 記録 + ETA、`run-all-core` を `scripts/ops/run_all.py` 化 + step 順修正 | ✅ 完了 2026-05-11 |
| `infra/` Phase 残骸 scrub | ~120 occurrence (コメント / description のみ) を固有名へ | ✅ 完了 2026-05-11 |
| ES production 化 (旧 M-Wave8.7) | HTTPS + password auth | ⏸ active backlog から外し parked → [`../backlog/production-hardening.md`](../backlog/production-hardening.md) |
| Helm provider 3.x 移行 | `~> 3.0` + `kubernetes = { }` 属性記法 | ⏸ 低優先 / スキップ可 (放置で致命的問題なし) |

完了済の詳細・証跡は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §6 / §7.3 / §7.4 を正本。次のアクティブ作業候補は §1 参照。

---

## §6. 関連ドキュメント

- [`TASKS.md`](TASKS.md) — current sprint
- [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) — canonical 仕様
- [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) — 実装スナップショット + マイルストーン履歴 + incident memo
- [`../runbook/04_検証.md`](../runbook/04_検証.md) / [`../runbook/05_運用.md`](../runbook/05_運用.md) — 検証 / PDCA
- [`../decisions/README.md`](../decisions/README.md) — ADR 0001〜0008
- [`../troubleshooting/`](../troubleshooting/) — incident memo (eck-license-reconcile-stall / terraform-lock-stale-after-bg-kill / bg-pipe-fake-exit-zero)
- [`../pmle-learning-notes.md`](../pmle-learning-notes.md) — PMLE 学習 doc (試験対策、本リポ実体験起点)
- [`../conventions/`](../conventions/) — 命名 / 配置 / Make / Docker 規約


これ、今からでもcsvに掛かった時間を記録する仕組みすべきだと思う
> それぞれに掛かった時間は計測しているよね
次にdeploy-allした時に、予測完了見込み時間を出せるように計測しているよね？