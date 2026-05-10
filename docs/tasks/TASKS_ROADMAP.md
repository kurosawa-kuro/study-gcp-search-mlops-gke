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
- GCP リソース識別子 (`phase7-synonym` Memorystore / `destroy-phase7-learning` Make target) は production リソース ID と Terraform 同期、touch すると infra との drift 発生 → 別 backlog
- M-Wave マイルストーンの Phase 1/2/3 (M-Wave8.6 Phase 1/2/3 等) は milestone 段階の固有名 = 撤廃対象外

### §0.2 仕様の大本命 (正解データ + 継続改善サイクル)

行動ログ → 正解データ → 再学習 → 評価 → deployment gate → KServe 反映 を 1 本の継続改善サイクルとして実装。アプリ側 (EventWriter Port) とモデル側 (`pipeline/training_job/main.py` の Repository 配線) の両方で正解データ対応。**M-Wave5 で 2026-05-10 完了**。

### §0.3 検索基盤 (Elasticsearch on GKE)

Meilisearch を廃止、GKE 上で Elasticsearch (ECK) を稼働。Elastic Cloud は不採用。**M-Wave6 で完了**、**M-Wave8.7 で HTTPS+password auth へ production 化** (backlog)。

---

## §1. 残課題 (current backlog)

| # | 残 | 関連 | 状態 |
|---|---|---|---|
| 1 | M-Wave7 Makefile 本格整理 (target rename / help 再生成 / 不要 target 撤去 / 規約 doc 同期) | §2 Wave 7 | ⏳ 着手可 |
| 2 | M-Wave8.6 Phase 2/3 後段 — caller migration (`subprocess.run(["kubectl"\|"terraform", ...])` → adapter 経由 ~30 箇所) | §2 Wave 8.6 | ⏳ 着手可 |
| 3 | M-Wave8.7 ES production 化 (HTTPS + password auth) | §2 Wave 8.7 | ⏸ ドメイン購入タイミング待ち |
| 4 | M-Wave9 独自ドメイン + HTTPS + DNS (Web 公開基盤) | §2 Wave 9 | ⏸ scope outside (user 指示) |
| 5 | GCP リソース ID rename (`phase7-synonym` Memorystore / `destroy-phase7-learning` Make target) | §0.1 例外 | ⏸ M-Wave8.5 残、infra 同期必要 |

完了済 Wave (0/1/2/3/4/5/6/8 / M-Pivot / M-RunbookLocal / M-Wave8.6 Phase 1-3 / M-Wave8.5 / Step.precondition framework / C4 Makefile python -u / PMLE doc) は [03_実装カタログ §7.3](../architecture/03_実装カタログ.md) を正本。

---

## §2. 残 Wave 詳細

### Wave 7 — Makefile / 実行系の本格整理

**目的**: Makefile を `make help` だけで全体把握できる canonical 状態に。Wave 0 (止血) 完了済。

**作業**:
- [ ] 全 Make target を canonical 命名規約 ([`docs/conventions/Makefile規約.md`](../conventions/Makefile規約.md) / [`スクリプト規約.md`](../conventions/スクリプト規約.md)) に揃える
- [ ] `tools/generate_makefile_md.sh` から `archive/1〜6` walk + Phase Support Matrix を撤去 (= M-Pivot 反映)
- [ ] `make help` の語彙再生成 (`tools/generate_makefile_md.sh` 実行)
- [ ] 不要 / 重複 / legacy target を撤去 (`up`/`down`/`db-migrate-*`/`seed`/`serve`/`eval-*` 等、本リポで未使用)
- [ ] 1 target = 1 行の `uv run python -u -m scripts.<folder>.<module>` 原則を全件適用
- [ ] **C5**: bg/pipe 系 target に `set -o pipefail` を SHELL 既定に (現状は `python -u` で line buffer のみ対応、pipefail は未対応)

**完了条件**: Makefile 内に多行 shell 0 件 (Wave 0 で達成済)、`docs/conventions/Makefile規約.md` の Make Command Matrix が現状と一致 + Phase Support Matrix なし。

---

### Wave 8.6 Phase 2/3 後段 — caller migration

**目的**: M-Wave8.6 Phase 1 (step 分離 / tf_apply.py 切り出し) / Phase 2 (`scripts/domain/{gcp,k8s,terraform}/` 再配置) / Phase 3 minimal (`scripts/adapters/{kubectl,gcloud,terraform}.py` 構造) は 2026-05-09/10 で完了。**残 = 既存 caller の subprocess 直書きを adapter 経由 migration**。

**作業**:
- [ ] `scripts/domain/gcp/state_recovery.py` 内 9 件の `subprocess.run(["gcloud", ...])` → `gcloud_run(...)`
- [ ] `scripts/domain/gcp/vertex_*.py` 内 3 件 + `scripts/domain/k8s/elasticsearch_wait.py` 内 2 件 → adapter 経由
- [ ] `scripts/setup/seed_minimal_clean.py` 3 件 (bq) / `scripts/_common.py` 内 3 件 → 順次
- [ ] `scripts/lib/*` を `scripts/domain/<topic>/` に整理 (現状残存)
- [ ] mypy + pytest で regression 0 確認

**完了条件**: `grep -rE 'subprocess\.run\(\["(kubectl|gcloud|terraform)"' scripts/` が ≤ 5 件 (adapters 内部実装を除く)。

---

### Wave 8.7 — ES production 化 (HTTPS + password auth)

**目的**: 学習用 (a') 解 (HTTP + anonymous superuser) を production grade へ移行。

**作業**:
- [ ] canonical URL を環境変数で http/https 切替 (`scripts/ops/sync_elasticsearch.py` / `infra/manifests/search-api/configmap.yaml`)
- [ ] ECK auto-generated `elasticsearch-es-elastic-user` secret から password fetch する経路を `_run_sync_elasticsearch` に組込
- [ ] `infra/manifests/elasticsearch/elasticsearch.yaml` の `xpack.security.authc.anonymous.*` 削除 → ECK default の HTTPS+auth へ
- [ ] [test_codebase_invariants.py](../../tests/integration/parity/test_codebase_invariants.py) の `test_es_manifest_pins_http_and_anonymous_auth` を HTTPS+auth pin に更新
- [ ] CLAUDE.md / README に「学習用 anonymous superuser は production 厳禁」を明記

**完了条件**: ES が default の HTTPS+auth で動作、`make verify-live-acceptance` PASS。**前提**: ドメイン購入タイミング (M-Wave9 と同時推奨)。

---

### Wave 9 — Web 公開基盤 (独自ドメイン + HTTPS + DNS)

**目的**: Web アプリを GCP 上で独自ドメイン配信、HTTPS/TLS + DNS を canonical 手順で固定。

**作業**:
- [ ] GCP (Cloud Domains) で公開用ドメインを購入
- [ ] Cloud DNS Public Zone 作成、購入ドメインの NS 委任
- [ ] Gateway リスナーに独自ドメイン host 追加、`HTTPRoute` の `hostnames` 一致
- [ ] Google-managed certificate を作成、Gateway にバインド
- [ ] `A/AAAA` (必要に応じて `CNAME`) を Gateway 外部 IP へ
- [ ] `curl -I https://<domain>` / `openssl s_client` / `make ops-search` で疎通検証

**完了条件**: 独自ドメイン経由で `/api/v1/search` が HTTPS 200 を返し、証明書が自動更新される。**scope outside** (user 指示で除外継続、ドメイン購入タイミングで着手)。

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
| M-Wave7 | Makefile 本格整理 | ⏳ 着手可 |
| M-Wave8.6 後段 | caller migration (subprocess → adapter) | ⏳ 着手可 |
| M-Wave8.7 | ES production 化 | ⏸ M-Wave9 と同時 |
| M-Wave9 | 独自ドメイン + HTTPS + DNS | ⏸ scope outside |

完了済は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §7.3 を正本。

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
