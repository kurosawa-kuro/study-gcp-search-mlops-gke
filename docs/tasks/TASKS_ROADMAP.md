# TASKS_ROADMAP

不動産ハイブリッド検索 + 継続改善 MLOps サイクルの **長期 backlog + 決定的仕様 + Wave 計画 + incident postmortem の母艦**。

権威順位: `TASKS_ROADMAP > TASKS > 01_仕様と設計 > README > CLAUDE`

---

## §0. プロジェクト方針

### §0.1 ピボット完了 (Phase 形式 → 個人技術学習プロジェクト)

チームメンバー向けの **Phase 1〜7 形式の学習資料はリリース済みで役目を終えた**。今後はその資産を活かしつつ、個人の技術学習プロジェクトとして、より深く柔軟に学習するため **教育用 Phase 形式 (Phase 1〜6 の段階的教材) を廃止**。

- ゴールの Phase 7 (= GKE + KServe + Composer + Vertex AI 一式) は repo ルートに昇格済み
- `1/` 〜 `6/` ディレクトリ、`docs/phases/`、`docs/教育資料/`、`archive/` は全て撤去済み
- README / CLAUDE / AGENTS から教育用 Phase 概念 (Phase 1〜6 段階教材) は撤去済み
- ⚠️ **`docs/architecture/01_仕様と設計.md §3` と `tests/integration/workflow/`** では **「Phase 7 で本実装、後方派生で Phase 6 へ引き算」** の wording が **Composer 配置設計の歴史的経緯名 / canonical 学習プロジェクト最終形態名** として残置 (workflow contract で pin)。これは教材としての段階廃止とは別の意図 (上下関係を表す固有名)、撤去対象ではない

### §0.2 仕様の大幅変更 (正解データ + 継続改善サイクル前提)

以前は正解データを度外視した設計だった。現在は **正解データとモデル品質改善サイクルを大前提とする仕様** に変更している。

- 行動ログ → 正解データ → 再学習 → 評価 → deployment gate → KServe 反映 を 1 本の継続改善サイクルとして実装する (詳細は本書 Wave 2-5)
- アプリ側 (EventWriter Port + structured log) とモデル側 (`pipeline/training_job/main.py` の Repository 配線) の両方で正解データ対応が必要

### §0.3 検索基盤の変更 (Meilisearch → Elasticsearch on GKE)

Meilisearch を廃止し、**Elasticsearch を採用** する。ただし Elastic Cloud は利用せず、**GKE 上で Elasticsearch を稼働** させる (詳細は本書 Wave 6)。

---

## §1. 今の課題 (Current Challenges)

| # | 課題 | 関連 doc | 状態 / スコープ |
|---|---|---|---|
| 1 | プロジェクト方針の変更 (Phase 形式廃止) | — | ✅ ピボット完了 |
| 2 | 仕様の大幅変更 (正解データ + 継続改善サイクル前提) | 本書 Wave 2-5 | ✅ 実装完了 / 🟡 Wave 5 live 検証 (`verify-live-acceptance`) 残件 |
| 3 | 検索基盤の変更 (Meilisearch → Elasticsearch on GKE) | 本書 Wave 6 | ✅ 完了 (`ops-search-components` all non-zero) |
| 4 | API エンドポイントの整理 (試行錯誤でつぎはぎ) | 本書 Wave 1 | ✅ 完了 (2026-05-09 contract test 9 件 PASS、03_実装カタログ §7.3) |
| 5 | Makefile / 実行系の破綻 (「コード直書き禁止」違反) | 本書 Wave 0 / 7 | 🟡 Wave 0 (止血) ✅ 完了 / Wave 7 (本格整理) ⏳ 着手可 |
| 6 | Web アプリ公開基盤の不足 (独自ドメイン + HTTPS + DNS) | [`docs/runbook/05_運用.md`](../runbook/05_運用.md) | ⏳ **scope outside (本 sprint)** — Wave 9 に分離。GCP でドメイン購入、証明書発行、DNS 委任、Gateway/HTTPRoute 反映 |

---

## §2. Wave 構成 (実施順)

仕様・API・実装方針を **正しい順序で固める** ことを優先する。Wave 0 は guardrail (止血)、Wave 1-5 は仕様 → アプリ → モデル → サイクル統合、Wave 6-8 はインフラ刷新と整理、Wave 9 は外部公開基盤の仕上げ。

### Wave 0 — Makefile 止血 (guardrail、Wave 1 着手前)

**目的**: Makefile に直書きされた多行 shell ブロックを scripts/ 経由に寄せる (危険箇所のみ)。Makefile 全体の本格整理は Wave 7。

**作業**:
- [ ] 本書に集約した違反観点 (Wave 0) で多行 shell 箇所を全件抽出
- [ ] 多行 shell が混入している target (`verify-deploy-all` / `verify-destroy-all` / `verify-live-acceptance` / `verify-full-recreate` / `ops-deploy-monitor` / `ops-run-all-monitor` 等) を `scripts/setup/verify_*.py` / `scripts/ops/*_monitor.py` に移送
- [ ] Makefile target は `uv run python -m scripts.<folder>.<module>` の 1 行 wrapper に統一
- [ ] 既存 contract test (`tests/integration/workflow/`) を破らないこと
- [ ] `make check` PASS

**完了条件**: Makefile 内に `\` 行継続で書かれた 5 行超の shell block が **0 件**。

---

### Wave 1 — API エンドポイント再設計 (仕様確定の起点)

**目的**: 正解データ / イベントログ / 再学習 / 評価 / Elasticsearch 連携を実装する **前に**、API 境界を 4 軸分離で一斉整理する。

**指針** (本書 Wave 1):

```
/api/v1/*      公開 API (エンドユーザー、契約・認証境界、バージョニング必須)
/ops/*         運用 API (開発者・運用者、IAP のみ、自由に進化)
/ui/*          Jinja UI (operator 用、IAP 配下)
/{livez,readyz,healthz,metrics}  k8s + Prometheus 予約
```

**作業**:
- [ ] 現状エンドポイント一覧を [`docs/architecture/03_実装カタログ.md` §4](../architecture/03_実装カタログ.md) と突き合わせ、4 軸へマッピング
- [ ] `/search` `/feedback` を `/api/v1/search` `/api/v1/feedback` へ rename (旧 path は 308 redirect で 1 sprint だけ残す)
- [ ] `/jobs/check-retrain` `/model/info` `/model/metrics` を `/ops/` 配下へ移送
- [ ] `infra/manifests/policies/search-api-iap-policy.yaml` の `GCPBackendPolicy` を prefix 単位で書き直し
- [ ] `tests/integration/parity/` に API 境界 contract を追加 (新 prefix が混在しないことを pin)
- [ ] [`docs/architecture/03_実装カタログ.md` §4 API エンドポイント](../architecture/03_実装カタログ.md) を更新

**完了条件**: 全 endpoint が 4 軸のいずれかに属し、prefix 違反 0 件。

---

### Wave 2 — 正解データの仕様確定

**目的**: Event schema / 重み付き relevance label / synthetic 注入の仕様を **コード・docs・YAML fixture で完全一致** させる。

**指針** (本書 Wave 2-5):

- Event schema 共通契約: `search_events` / `search_impressions` / `user_actions` の 3 テーブル
- `action_type` enum 8 種: アプリ emit 5 種 (`click` / `detail_view` / `favorite` / `request_button_click` / `request_complete`) + synthetic 注入専用 3 種 (`inquiry_complete` / `contract` / `bounce`)
- 重み付き relevance label: `click`=1, `detail_view`=2, `favorite`=3, `request_button_click`=4, `request_complete`=5, `inquiry_complete`=7, `contract`=10, `no_action`=0, `bounce`=0/-1

**作業**:
- [x] 実装・検証完了（詳細ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)）

**完了条件**: 6 つの canonical 場所 (Pydantic / Terraform / labeling YAML / labeling SQL / EventWriter Port / `ranking_labels` 書き込み) で `action_type` enum と weight が一致。

---

### Wave 3 — アプリ側の正解データログ実装

**目的**: search-api が Event schema 共通契約に従って構造化ログを Cloud Logging に流し、BQ Subscription 経由で BigQuery curated tables に着地する経路を完成させる。

**指針** (本書 Wave 2-5):

- `EventWriter` Port + `cloud_logging_event_writer` adapter (search-api on GKE 用)
- `EventRepository` Port + `bigquery_event_repository` adapter (Composer DAG が呼ぶ)
- 物件詳細ページの最小 UI 導線 (`detail_view` / `favorite` / `request_button_click` / `request_complete` を emit)

**作業**:
- [x] 実装・検証完了（詳細ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)）

**完了条件**: `/api/v1/feedback` 呼び出しが Cloud Logging → BQ Subscription → BigQuery `mlops.user_actions` まで到達することを `make ops-feedback` smoke で確認。

---

### Wave 4 — モデル側の学習データ反映 (LightGBM 接続死守ライン)

**目的**: ⚠️ **canonical 死守ライン** — `pipeline/training_job/main.py` から `ml/data/loaders/ranker_repository.py` (BigQuery loader、実装済) を呼ぶ配線実装を完了させる。

**指針** (本書 Wave 2-5):

**作業**:
- [x] 実装・検証完了（詳細ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)）

**完了条件**: 実 BigQuery `ranking_labels` 由来の training dataset で LightGBM が学習し、新 model version が Vertex Model Registry に登録されること。

---

### Wave 5 — 継続改善サイクル MVP

**目的**: Composer DAG 3 本 (`daily_feature_refresh` / `retrain_orchestration` / `monitoring_validation`) が継続改善サイクルを駆動し、deployment gate 評価で promote 判定が出て KServe storageUri が新 model artifact を指すまでを完走させる。

**指針** (本書 Wave 5):

```
search-api → event logs → BigQuery curated → Composer (retrain_orchestration)
  → labeling SQL → ranking_labels → training dataset
  → Vertex Pipelines retrain → Vertex Model Registry
  → deployment gate (NDCG@10 / Recall@K / CTR / CVR を evaluation_metrics に保存)
  → KServe storageUri patch (新 model artifact 反映)
```

**作業**:
- [x] 実装・検証完了（詳細ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)）

**完了条件**: `make verify-live-acceptance` が継続改善サイクル完走を含めて PASS する。3 系統 all non-zero + Vertex Vector Search 実検索 + Feature View 経由 fetch + KServe 経由 rerank + deployment gate promote 判定 + KServe storageUri 反映までが 1 本線で動く。

---

### Wave 6 — Elasticsearch 移行 (GKE 上)

**目的**: Meilisearch を廃止し、GKE 上で Elasticsearch を稼働させる。Cloud Run / Elastic Cloud / Cloud Build 案は不採用。

**進捗**: **実装・検証完了**（詳細ログは [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md)）。

**完了条件**: `/api/v1/search` の lexical 経路が ES 由来で動作し、3 系統 all non-zero が ES + VVS + KServe で成立。Meilisearch リソースが Terraform / manifests から削除済。

---

### Wave 7 — Makefile / 実行系の本格整理

**目的**: Wave 0 の止血を超えて、Makefile を `make help` だけで全体把握できる状態にする。仕様・API・実装方針が Wave 1-6 で固まったあとに着手。

**作業**:
- [ ] 全 Make target を canonical 命名規約 ([`docs/conventions/Makefile規約.md`](../conventions/Makefile規約.md) + [`docs/conventions/スクリプト規約.md`](../conventions/スクリプト規約.md)) に揃える
- [ ] 1 target = 1 行の `uv run python -m scripts.<folder>.<module>` 原則を全件適用
- [ ] `make help` の語彙を再生成 (`tools/generate_makefile_md.sh`)
- [ ] 不要 / 重複 / legacy target を撤去
- [ ] **2026-05-10 incident 反映**: bg/pipe 系 target (`deploy-all` / `destroy-all` / `verify-live-acceptance` 等) に `stdbuf -oL -eL` を wrap して line buffer 化、`set -o pipefail` を SHELL 既定に。Bash tool 側で毎回 `bash -c 'set -o pipefail; ... \| stdbuf -oL -eL tee ...'` を書く運用負荷を消す

**完了条件**: Makefile 内に多行 shell が 0 件。`docs/conventions/Makefile規約.md` の Make Command Matrix が現状と一致。

---

### Wave 8 — ドキュメント再統合

**目的**: Wave 1-7 の成果を canonical docs に反映し、新しい仕様・実装で `01_仕様と設計.md` / `03_実装カタログ.md` / `runbook/05_運用.md` / `runbook/04_検証.md` が drift なく揃った状態にする。

**現在地 (2026-05-06 21:12 JST)**: `make check` は **779 passed / 2 skipped / 0 failed**。残件は runbook 2 本の最終同期と live acceptance 最終通し。

**作業**:
- [x] [`docs/architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) を Wave 1-6 の最終仕様に追従
- [x] [`docs/architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) を Elasticsearch / 4 軸 API / 新 Port / 配線実装で更新
- [ ] [`docs/runbook/05_運用.md`](../runbook/05_運用.md) を新 PDCA 本線で書き直し
- [ ] [`docs/runbook/04_検証.md`](../runbook/04_検証.md) の検証ゲートを継続改善サイクル完走基準で更新
- [x] `infra/terraform/modules/elasticsearch/` に `outputs.tf` / `versions.tf` を追加し module 4 ファイル契約を回復
- [x] `scripts/deploy/configmap_overlay.py` の ES URL 既定値と workflow contract の期待値 (`http://...`) を一致させる
- [x] `docs/architecture/01_仕様と設計.md` に workflow contract 必須文言 (見出し + Composer canonical wording) を復元
- [x] `docs/architecture/03_実装カタログ.md` に `sync-elasticsearch` canonical 表記を追加
- [x] `infra/run/services/reranker/Dockerfile` に apt cache mount (`--mount=type=cache,target=/var/cache/apt,sharing=locked`) を反映
- [x] 設計メモ群を `TASKS_ROADMAP.md` / `TASKS.md` に集約し、個別メモファイルを削除

**完了条件**: `tasks/TASKS_ROADMAP.md` の「今の課題」6 件がすべて解消され、本 doc の記述と canonical docs (01 / 03 / runbook) が一致。

> Wave 8 収束トリオ (Terraform module structure / deploy-all workflow contract / docs canonical contract / reranker image) は完了済。詳細は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §7.2 を正本とする。

---

### Wave 8.7 — ES production 化 (HTTPS + password auth)

**目的**: 2026-05-10 incident 解消で採用した (a') 解 = HTTP + anonymous superuser は **学習プロジェクト前提** (CLAUDE.md「個人技術学習プロジェクト」)。production 配信や client 公開フェーズで使う場合は HTTPS + password auth へ移行する必要がある。

**残件 (= production 化のための作業)**:
- [ ] canonical URL を環境変数で http/https 切替可能に (`scripts/ops/sync_elasticsearch.py` / `infra/manifests/search-api/configmap.yaml`)
- [ ] ECK auto-generated `elasticsearch-es-elastic-user` secret から password fetch する経路を `_run_sync_elasticsearch` に組込
- [ ] `infra/manifests/elasticsearch/elasticsearch.yaml` の `xpack.security.authc.anonymous.*` を削除 → ES manifest を default の HTTPS+auth へ戻す
- [ ] Wave 8 contract test (`test_docs_runbook_and_catalog_pin_elasticsearch_workflow`) を **HTTPS + auth header 対応** に拡張
- [ ] [tests/integration/parity/test_codebase_invariants.py](../../tests/integration/parity/test_codebase_invariants.py) の `test_es_manifest_pins_http_and_anonymous_auth` を更新
- [ ] CLAUDE.md / README に「学習用 anonymous superuser は production 厳禁」を明記

**完了条件**: ES が default の HTTPS+auth で動作、`make verify-live-acceptance` PASS、上記 contract test がすべて HTTPS+password auth pin に変更され `make check` PASS。

**前提**: 学習用 deploy-all が本 sprint で安定動作することが前提 (T1 PASS)。

---

### Wave 8.6 — orchestrator のドメイン分離 (クリーンアーキテクチャ整理)

**目的**: 2026-05-09 incident (`--from-step tf-apply` で step 3 skip → WIF 409 → 30+ 分の出戻り) を発端に、`scripts/setup/{deploy_all,destroy_all}.py` の構造再編を進めた。Phase 1 (step 分離 + slicing 対称化、tf_apply.py 切り出し、idempotent 前置き hook、contract test 化) は M-Wave8 内で完了。Phase 2/3 のドメイン分離が残件。

**残件 (Phase 2/3)**:
- [ ] `scripts/infra/*` を `scripts/domain/{gcp,k8s,terraform,data}/` に再配置 (state_recovery / vertex_cleanup / vertex_import / kubectl_context / terraform_lock 等)
- [ ] `scripts/lib/*` を `scripts/domain/<topic>/` または `scripts/adapters/` に整理
- [ ] gcloud / kubectl / terraform subprocess wrapper を `scripts/adapters/` に分離 (mock 容易化)
- [ ] 影響範囲: `Makefile` / `tests/` / 内部 import ~30+ 箇所の追従更新

**完了条件**: クリーンアーキテクチャ 4 層 (orchestration / domain / adapters / infra-config) が `scripts/` 配下で見える階層化、`make check` PASS、`scripts/setup/{deploy_all,destroy_all}.py` が thin orchestrator のまま。

**前提**: Wave 7 (Makefile 本格整理) と並行可能だが、import path 一斉変更を伴うため別 sprint 推奨。

---

### Wave 8.5 — Phase 概念の完全撤廃 (canonical wording を Phase 7/6 から固有名へ)

**目的**: 本リポは Phase 分裂教材ではなく、教育用 Phase 1〜6 教材は M-Pivot で撤去済。残った「Phase 7 で本実装、後方派生で Phase 6 へ引き算」(`docs/architecture/01_仕様と設計.md §3` / `tests/integration/workflow/` 15+ ファイル / `docs/runbook/{04,05}.md` 数十箇所) は **Composer 配置設計の上下関係を表す** ためだけに残っている wording。固有名化 (例: 「canonical (= GKE + KServe + Composer 一式)」「Composer なし派生」) で完全撤廃する。

**作業**:
- [ ] `docs/architecture/01_仕様と設計.md §3` の Phase 7/6 wording を canonical / Composer なし派生 等の固有名へ書き換え
- [ ] `tests/integration/workflow/` 15+ ファイルの docstring + pin assertion から `Phase [0-9]` を撤去 (canonical 意図は別 wording で保持)
- [ ] `docs/runbook/04_検証.md` / `docs/runbook/05_運用.md` の Phase 表記を canonical wording に置換
- [ ] `docs/architecture/03_実装カタログ.md` / `docs/tasks/TASKS_ROADMAP.md §0.1` の経緯メモを最終形態に更新
- [ ] `make check` PASS

**完了条件**: `grep -rE "Phase [0-9]" docs/ tests/integration/workflow/` が **0 件**。canonical 仕様 §3 が「Composer = 上位 orchestrator、Vertex Pipelines = 下位 ML executor」を Phase 表記なしで表現できている。

**前提**: Wave 8 完了 (= 現 sprint の T1/T2 が ✅) 後に着手。本 Wave は意図的に大量 Edit を伴うため、`verify-live-acceptance` PASS 後に 1 sprint 切って実施する。

---

### Wave 9 — Web 公開基盤 (独自ドメイン + HTTPS + DNS)

**目的**: Web アプリを GCP 上で独自ドメイン配信し、HTTPS/TLS と DNS を canonical 手順で固定する。

**作業**:
- [ ] GCP (Cloud Domains もしくは同等手段) で公開用ドメインを購入
- [ ] Cloud DNS Public Zone を作成し、購入ドメインの NS を委任
- [ ] Gateway のリスナーに独自ドメイン host を追加し、`HTTPRoute` の `hostnames` を一致させる
- [ ] Google-managed certificate (または Certificate Manager) を作成し、Gateway にバインド
- [ ] `A/AAAA` (必要に応じて `CNAME`) を Gateway 外部IPへ向ける
- [ ] `curl -I https://<domain>` / `openssl s_client` / `make ops-search` で証明書と疎通を検証

**完了条件**: 独自ドメイン経由で `/api/v1/search` が HTTPS 200 を返し、証明書が有効で自動更新される。

---

## §3. 不変ルール / 非負制約

### §3.1 ⛔ ゴール劣化禁止 (= クライアント罰金回避ライン)

「**本線**」「**必須**」「**canonical**」「**不変**」と書かれた要件 (中核 5 要素 / Composer = 上位 orchestrator / 本線 retrain DAG / Feature View 経由 fetch / Wave 4 LightGBM 接続死守ライン / 等) を **未達のまま「完了」「OK」と扱うのは禁止**。

**禁止する hedging 表現**:
- 「深追いは別 sprint (候補)」
- 「現状で W2-X 完了とみなし、次のステージへ進む」
- 「Stage X.Y 未解決のまま完了扱い」
- canonical 必須項目に対する「task SUCCEEDED は別 sprint」「live verify は別 session」「明日以降」「後追い」
- 判断 A/B が並列に書かれている場合、勝手に A を選んで B を「別 sprint」へ送る (User 明示確認なし)

**正しい扱い方**:
1. canonical 未達は ⚠️ マーカー付きで「**canonical 未達 (= ゴール劣化)、追加 sprint 必須**」と明示
2. canonical 必須項目と機能影響低の項目を **明確に区別**
3. canonical 違反が生じる選択肢は ~~取り消し線~~ で不採用宣言
4. 「Wave X 完了」を書く前に、本ファイル §3 / [`docs/architecture/01_仕様と設計.md §0.1`](../architecture/01_仕様と設計.md) と **必ず照合**

### §3.2 中核 5 要素

- **不変**: multilingual-e5 + RRF + LightGBM LambdaRank
- **置換中 (Wave 6)**: Meilisearch BM25 → **Elasticsearch BM25**
- **不変**: Vertex AI Vector Search (ME5 ベクトル serving index、source は BigQuery 側 embedding テーブル)

### §3.3 LightGBM 接続死守ライン (Wave 4)

`pipeline/training_job/main.py` から `ml/data/loaders/ranker_repository.py` (BigQuery loader) を呼ぶ配線実装が完了していない限り、Composer DAG が幾ら trigger しても LightGBM は乱数学習のまま。**Wave 4 完了条件を欺かない**。

### §3.4 Composer × Vertex Pipelines は上下関係

Composer = 上位 orchestrator、Vertex Pipelines = 下位 ML executor。`train/evaluate/register` を Composer 側に書かない (カニバリ禁止)。Vertex `PipelineJobSchedule` は併存禁止。Cloud Scheduler / Eventarc / Cloud Function (Gen2) trigger は本線から外し、smoke / manual trigger 用途として残置のみ。詳細は [`docs/architecture/01_仕様と設計.md §2`](../architecture/01_仕様と設計.md)。

### §3.5 incident postmortem は contract test として固定化

過去 incident (`prevent_destroy` 失敗 / tfstate orphan 151 件 / `state_recovery.py` 12 type 拡張 / Composer DAG `retrain_orchestration::check_retrain` SUCCEEDED 未達 hedging) は `tests/integration/workflow/test_destroy_all_contract.py` などに **15 件以上の contract test** として固定化済み。新 incident も同パターンで固定化する。

---

## §4. リスクと回避

| リスク | 回避 |
|---|---|
| Wave の並行実施で API 境界が複数版混在する | Wave 1 (API 再設計) を **必ず先に固める**。Wave 2-5 は新 prefix を前提に実装 |
| Wave 4 (LightGBM 接続) を「Wave 5 で代替できる」と勘違いし飛ばす | §3.3 死守ライン明記。Wave 4 完了条件 = 実 BigQuery `ranking_labels` 由来 retrain が Vertex Model Registry に登録 |
| Wave 6 (ES 移行) で同義語辞書 (`SynonymExpanderPort`) を破壊する | Redis 経路は Wave 6 でも維持、`MeilisearchAdapter` ↔ `ElasticsearchAdapter` の差し替えだけで完結する設計 |
| Wave 7 (Makefile 整理) を Wave 1-6 と同時に走らせ、検証経路が壊れる | 仕様・API・実装方針が固まる Wave 6 完了後にのみ着手 |
| deployed_index 残置による Vertex Vector Search 課金事故 (1 replica = ¥1,460/日) | `make destroy-all` で能動 undeploy + Cloud Scheduler 自動 undeploy (backlog) + Billing Budget Alert (backlog) |

### 4.9 Vertex Vector Search 永続化 lessons learned

2026-05-03 incident では Terraform destroy 中に `Instance cannot be destroyed` が発生し、Index / Endpoint の保護に `prevent_destroy` を使う設計が本線 teardown と衝突した。以後は **`prevent_destroy` を採用しない**。

採用した置換パターン:

- `destroy-all` で永続化したい VVS リソースは `state rm` で tfstate から外す
- 次回 `deploy-all` では必要に応じて `terraform import` で state 復帰する
- bare `state rm` を乱用せず、runbook に従って `state-recover` と対で扱う

この方針で `destroy-all` の no-prompt 性を守りつつ、GCP 側に残したい Index / Endpoint を扱う。将来さらに保護を強める backlog としては **Stack 分離**、**Cloud Scheduler 自動 undeploy**、Billing Alert、health check 強化を残す。

---

## §5. マイルストーン

完了済 (M-Pivot / M-RunbookLocal / M-Wave0 / M-Wave1 / M-Wave2 / M-Wave3 / M-Wave4 / M-Wave6) は [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) §7.3 を正本とする。本表は **未完了 / 進行中のみ** 残す。

| ID | フェーズ | 状態 | 残件 / 着手リンク |
|---|---|---|---|
| ~~M-Wave5~~ | 継続改善サイクル MVP | ✅ **完了 (2026-05-10)** | `make verify-live-acceptance` PASS (e2e 22.68s)。canonical 経路全動作。詳細: 03_実装カタログ §7.3 |
| M-Wave7 | Makefile 本格整理 | ⏳ 着手可 | Wave 0 / Wave 1 完了済。Make Command Matrix と Makefile を一致させる |
| M-Wave8.5 | Phase 概念の完全撤廃 | ⏳ | Wave 8 完了済 (drift 解消は 03_実装カタログ §7.3)。残: 01 §3 / workflow contract test 15+ / runbook の `Phase [0-9]` を固有名 (canonical / Composer なし派生) へ置換。詳細は §2 Wave 8.5 |
| M-Wave8.6 | orchestrator のドメイン分離 | ⏳ | Phase 1 (step 分離 + tf_apply.py 切り出し + 対称化) 完了 (2026-05-09)。残: `scripts/infra/*` → `scripts/domain/{gcp,k8s,terraform,data}/` 再配置、subprocess wrapper を `scripts/adapters/` に分離。詳細は §2 Wave 8.6 |
| M-Wave8.7 | ES production 化 (HTTPS + password auth) | ⏳ scope outside (学習プロジェクト前提で本 sprint 除外) | 2026-05-10 incident で採用した HTTP + anonymous superuser は学習用。production 配信時に HTTPS + password auth へ移行。詳細は §2 Wave 8.7 |
| M-Wave9 | 独自ドメイン + HTTPS + DNS | ⏳ scope outside | 本 sprint 除外 (user 指示)。詳細は §2 Wave 9 |

---

## §6. 関連ドキュメント

### §6.1 設計メモ統合

- 2026-05-06 に、設計メモ群は `TASKS_ROADMAP.md` / `TASKS.md` へ集約済み。
- 今後の作業・判断・履歴は本ファイルと `TASKS.md` を正本とする。

### §6.2 canonical docs

- [`TASKS.md`](TASKS.md) — current sprint dashboard (新セッションが最初に読む)
- [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) — canonical 仕様
- [`../architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) — 実装スナップショット
- [`../runbook/05_運用.md`](../runbook/05_運用.md) — PDCA / runbook
- [`../runbook/04_検証.md`](../runbook/04_検証.md) — 検証ゲート定義 (V1-V6)
- [`../decisions/README.md`](../decisions/README.md) — ADR 0001〜0008
- [`../conventions/`](../conventions/) — 命名 / 配置 / Make / Docker 規約

### §6.3 リポジトリ起点

- [`../../README.md`](../../README.md) — プロジェクト概要 + 技術スタック + 非負制約
- [`../../CLAUDE.md`](../../CLAUDE.md) — Claude Code 向けガイド
- [`../../AGENTS.md`](../../AGENTS.md) — Cursor / Codex 向け charter