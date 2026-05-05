# TASKS_ROADMAP

不動産ハイブリッド検索 + 継続改善 MLOps サイクルの **長期 backlog + 決定的仕様 + Wave 計画 + incident postmortem の母艦**。

権威順位: `TASKS_ROADMAP > TASKS > 01_仕様と設計 > README > CLAUDE`

---

## §0. プロジェクト方針

### §0.1 ピボット完了 (Phase 形式 → 個人技術学習プロジェクト)

チームメンバー向けの **Phase 1〜7 形式の学習資料はリリース済みで役目を終えた**。今後はその資産を活かしつつ、個人の技術学習プロジェクトとして、より深く柔軟に学習するため **Phase 形式を廃止**。

- ゴールの Phase 7 (= GKE + KServe + Composer + Vertex AI 一式) は repo ルートに昇格済み
- `1/` 〜 `6/` ディレクトリ、`docs/phases/`、`docs/教育資料/`、`archive/` は全て撤去済み
- 主要ドキュメント (README / CLAUDE / AGENTS / docs/architecture/01 / 03) から Phase 概念は撤去済み

### §0.2 仕様の大幅変更 (正解データ + 継続改善サイクル前提)

以前は正解データを度外視した設計だった。現在は **正解データとモデル品質改善サイクルを大前提とする仕様** に変更している。

- 行動ログ → 正解データ → 再学習 → 評価 → deployment gate → KServe 反映 を 1 本の継続改善サイクルとして実装する (詳細は [`継続改善サイクル設計.md`](継続改善サイクル設計.md))
- アプリ側 (EventWriter Port + structured log) とモデル側 (`pipeline/training_job/main.py` の Repository 配線) の両方で正解データ対応が必要

### §0.3 検索基盤の変更 (Meilisearch → Elasticsearch on GKE)

Meilisearch を廃止し、**Elasticsearch を採用** する。ただし Elastic Cloud は利用せず、**GKE 上で Elasticsearch を稼働** させる (詳細は [`Elasticsearch-GCP稼働先比較.md`](Elasticsearch-GCP稼働先比較.md))。

---

## §1. 今の課題 (Current Challenges)

| # | 課題 | 関連 doc | スコープ |
|---|---|---|---|
| 1 | プロジェクト方針の変更 (Phase 形式廃止) | — | ✅ ピボット完了 (本 sprint) |
| 2 | 仕様の大幅変更 (正解データ + 継続改善サイクル前提) | [`継続改善サイクル設計.md`](継続改善サイクル設計.md) / [`正解データ反映計画.md`](正解データ反映計画.md) | アプリ側 + モデル側の両方で正解データ対応 |
| 3 | 検索基盤の変更 (Meilisearch → Elasticsearch on GKE) | [`Elasticsearch-GCP稼働先比較.md`](Elasticsearch-GCP稼働先比較.md) | LexicalSearchPort の adapter 差し替え + GKE 上 ES 稼働 |
| 4 | API エンドポイントの整理 (試行錯誤でつぎはぎ) | [`APIエンドポイント再設計案.md`](APIエンドポイント再設計案.md) | `/api/v1/` `/ops/` `/ui/` `/` 4 軸分離 |
| 5 | Makefile / 実行系の破綻 (「コード直書き禁止」違反) | [`Makefile-多行禁止違反メモ.md`](Makefile-多行禁止違反メモ.md) | 危険箇所の止血のみ先行、本格整理は仕様確定後 |

---

## §2. Wave 構成 (実施順)

仕様・API・実装方針を **正しい順序で固める** ことを優先する。Wave 0 は guardrail (止血)、Wave 1-5 は仕様 → アプリ → モデル → サイクル統合、Wave 6-8 はインフラ刷新と整理。

### Wave 0 — Makefile 止血 (guardrail、Wave 1 着手前)

**目的**: Makefile に直書きされた多行 shell ブロックを scripts/ 経由に寄せる (危険箇所のみ)。Makefile 全体の本格整理は Wave 7。

**作業**:
- [ ] [`Makefile-多行禁止違反メモ.md`](Makefile-多行禁止違反メモ.md) で指摘された違反箇所を grep で全件抽出
- [ ] 多行 shell が混入している target (`verify-deploy-all` / `verify-destroy-all` / `verify-live-acceptance` / `verify-full-recreate` / `ops-deploy-monitor` / `ops-run-all-monitor` 等) を `scripts/setup/verify_*.py` / `scripts/ops/*_monitor.py` に移送
- [ ] Makefile target は `uv run python -m scripts.<folder>.<module>` の 1 行 wrapper に統一
- [ ] 既存 contract test (`tests/integration/workflow/`) を破らないこと
- [ ] `make check` PASS

**完了条件**: Makefile 内に `\` 行継続で書かれた 5 行超の shell block が **0 件**。

---

### Wave 1 — API エンドポイント再設計 (仕様確定の起点)

**目的**: 正解データ / イベントログ / 再学習 / 評価 / Elasticsearch 連携を実装する **前に**、API 境界を 4 軸分離で一斉整理する。

**指針** ([`APIエンドポイント再設計案.md` §1](APIエンドポイント再設計案.md)):

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

**指針** ([`継続改善サイクル設計.md` §5-§6](継続改善サイクル設計.md) + [`正解データ反映計画.md` §2-§3](正解データ反映計画.md)):

- Event schema 共通契約: `search_events` / `search_impressions` / `user_actions` の 3 テーブル
- `action_type` enum 8 種: アプリ emit 5 種 (`click` / `detail_view` / `favorite` / `request_button_click` / `request_complete`) + synthetic 注入専用 3 種 (`inquiry_complete` / `contract` / `bounce`)
- 重み付き relevance label: `click`=1, `detail_view`=2, `favorite`=3, `request_button_click`=4, `request_complete`=5, `inquiry_complete`=7, `contract`=10, `no_action`=0, `bounce`=0/-1

**作業**:
- [ ] `definitions/labeling/synthetic_actions.yaml` を canonical fixture として固定
- [ ] BigQuery `search_events` / `search_impressions` / `user_actions` / `ranking_labels` / `training_dataset` / `evaluation_metrics` のスキーマを Terraform `infra/terraform/modules/data/` で宣言
- [ ] Pydantic `FeedbackRequest.action` を Literal 5 種に絞り、4 種をアプリ経路で弾く
- [ ] `tests/integration/parity/` に Event schema 整合性 contract を追加 (Python ↔ Terraform ↔ YAML ↔ Pydantic の lock-step)

**完了条件**: 6 つの canonical 場所 (Pydantic / Terraform / labeling YAML / labeling SQL / EventWriter Port / `ranking_labels` 書き込み) で `action_type` enum と weight が一致。

---

### Wave 3 — アプリ側の正解データログ実装

**目的**: search-api が Event schema 共通契約に従って構造化ログを Cloud Logging に流し、BQ Subscription 経由で BigQuery curated tables に着地する経路を完成させる。

**指針** ([`正解データ反映計画.md` §3.1-§3.2](正解データ反映計画.md)):

- `EventWriter` Port + `cloud_logging_event_writer` adapter (search-api on GKE 用)
- `EventRepository` Port + `bigquery_event_repository` adapter (Composer DAG が呼ぶ)
- 物件詳細ページの最小 UI 導線 (`detail_view` / `favorite` / `request_button_click` / `request_complete` を emit)

**作業**:
- [ ] `app/services/protocols/event_writer.py` 新設 + `app/services/adapters/cloud_logging_event_writer.py`
- [ ] `app/services/protocols/event_repository.py` 新設 + `app/services/adapters/bigquery_event_repository.py`
- [ ] `app/api/routers/feedback_router.py` を Wave 1 の新 prefix (`/api/v1/feedback`) に合わせる
- [ ] `composition_root.py` で DI 配線 + `tests/_fakes/` に InMemory 版
- [ ] `scripts/ci/layers.py` の RULES に新 Port を追加

**完了条件**: `/api/v1/feedback` 呼び出しが Cloud Logging → BQ Subscription → BigQuery `mlops.user_actions` まで到達することを `make ops-feedback` smoke で確認。

---

### Wave 4 — モデル側の学習データ反映 (LightGBM 接続死守ライン)

**目的**: ⚠️ **canonical 死守ライン** — `pipeline/training_job/main.py` から `ml/data/loaders/ranker_repository.py` (BigQuery loader、実装済) を呼ぶ配線実装を完了させる。

**指針** ([`正解データ反映計画.md` §3.3-§3.4](正解データ反映計画.md)):

現状 `pipeline/training_job/main.py` は `synthetic_ranking_frames(seed=42)` で乱数学習しており、`ranking_labels` 未接続。Composer DAG が幾ら trigger しても、配線実装が完了しない限り **正解データは Vertex Pipelines retrain に届かない** (= Composer 本線化の意義が根幹で破綻)。

**作業**:
- [ ] `pipeline/training_job/main.py` で `ranker_repository.read_training_data(...)` を呼んで実 df を取得
- [ ] `trainer.run(df=df)` に渡す配線実装。`run(df=None)` 経路 (synthetic) は CI 専用に分離
- [ ] `LabelRepository` Port + `bigquery_label_repository` adapter (Composer DAG `retrain_orchestration` が labeling SQL → `ranking_labels` を作成)
- [ ] `TrainingDatasetRepository` Port + `gcs_training_dataset_repository` adapter

**完了条件**: 実 BigQuery `ranking_labels` 由来の training dataset で LightGBM が学習し、新 model version が Vertex Model Registry に登録されること。

---

### Wave 5 — 継続改善サイクル MVP

**目的**: Composer DAG 3 本 (`daily_feature_refresh` / `retrain_orchestration` / `monitoring_validation`) が継続改善サイクルを駆動し、deployment gate 評価で promote 判定が出て KServe storageUri が新 model artifact を指すまでを完走させる。

**指針** ([`継続改善サイクル設計.md` §11](継続改善サイクル設計.md) + [`正解データ反映計画.md` §3.4-§3.5](正解データ反映計画.md)):

```
search-api → event logs → BigQuery curated → Composer (retrain_orchestration)
  → labeling SQL → ranking_labels → training dataset
  → Vertex Pipelines retrain → Vertex Model Registry
  → deployment gate (NDCG@10 / Recall@K / CTR / CVR を evaluation_metrics に保存)
  → KServe storageUri patch (新 model artifact 反映)
```

**作業**:
- [ ] Composer DAG `retrain_orchestration` で Wave 4 配線実装を経由した実 retrain を 1 周走らせる
- [ ] `monitoring_validation` DAG で `evaluation_metrics` を計算 + deployment gate 判定
- [ ] `MetricsRepository` Port + `bigquery_metrics_repository` adapter
- [ ] [`継続改善サイクル設計.md` §9](継続改善サイクル設計.md) の `/admin/mlops` 1 ページを Wave 1 の `/ops/admin/mlops` 配下に追加 (ログ件数 / label 作成状況 / dataset 作成状況 / 評価指標 / deployment gate 結果 / 現行モデル情報)

**完了条件**: `make verify-live-acceptance` が継続改善サイクル完走を含めて PASS する。3 系統 all non-zero + Vertex Vector Search 実検索 + Feature View 経由 fetch + KServe 経由 rerank + deployment gate promote 判定 + KServe storageUri 反映までが 1 本線で動く。

---

### Wave 6 — Elasticsearch 移行 (GKE 上)

**目的**: Meilisearch を廃止し、GKE 上で Elasticsearch を稼働させる。Cloud Run / Elastic Cloud / Cloud Build 案は不採用 (詳細は [`Elasticsearch-GCP稼働先比較.md`](Elasticsearch-GCP稼働先比較.md))。

**作業**:
- [ ] ECK (Elastic Cloud on Kubernetes) Operator を `infra/terraform/modules/elasticsearch/` で導入 (Helm provider)
- [ ] `infra/manifests/elasticsearch/` に `Elasticsearch` CR + `Kibana` CR + PVC + NetworkPolicy
- [ ] `app/services/adapters/elasticsearch_lexical.py::ElasticsearchLexical` 実装 (`LexicalSearchPort` を satisfy、フィルタは structured DSL に翻訳)
- [ ] `composition_root.py` で `MeilisearchAdapter` → `ElasticsearchAdapter` 切替 (env flag で段階移行)
- [ ] Redis 同義語辞書 (`SynonymExpanderPort`) は ES 経路でも継続使用 (BM25 投入直前の query expansion は変えない)
- [ ] `scripts/ops/sync_elasticsearch.py` 新設 (`feature_mart.properties_cleaned` → ES index 同期)
- [ ] Meilisearch 関連リソース (`infra/terraform/modules/meilisearch/` + Cloud Run service + GCS FUSE bucket) を撤去
- [ ] [`docs/architecture/01_仕様と設計.md §1`](../architecture/01_仕様と設計.md) と §3 を ES に書き換え

**完了条件**: `/api/v1/search` の lexical 経路が ES 由来で動作し、3 系統 all non-zero が ES + VVS + KServe で成立。Meilisearch リソースが Terraform / manifests から削除済。

---

### Wave 7 — Makefile / 実行系の本格整理

**目的**: Wave 0 の止血を超えて、Makefile を `make help` だけで全体把握できる状態にする。仕様・API・実装方針が Wave 1-6 で固まったあとに着手。

**作業**:
- [ ] 全 Make target を canonical 命名規約 ([`docs/conventions/Makefile規約.md`](../conventions/Makefile規約.md) + [`docs/conventions/スクリプト規約.md`](../conventions/スクリプト規約.md)) に揃える
- [ ] 1 target = 1 行の `uv run python -m scripts.<folder>.<module>` 原則を全件適用
- [ ] `make help` の語彙を再生成 (`tools/generate_makefile_md.sh`)
- [ ] 不要 / 重複 / legacy target を撤去

**完了条件**: Makefile 内に多行 shell が 0 件。`docs/conventions/Makefile規約.md` の Make Command Matrix が現状と一致。

---

### Wave 8 — ドキュメント再統合

**目的**: Wave 1-7 の成果を canonical docs に反映し、新しい仕様・実装で `01_仕様と設計.md` / `03_実装カタログ.md` / `runbook/05_運用.md` / `runbook/04_検証.md` が drift なく揃った状態にする。

**作業**:
- [ ] [`docs/architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md) を Wave 1-6 の最終仕様に追従
- [ ] [`docs/architecture/03_実装カタログ.md`](../architecture/03_実装カタログ.md) を Elasticsearch / 4 軸 API / 新 Port / 配線実装で更新
- [ ] [`docs/runbook/05_運用.md`](../runbook/05_運用.md) を新 PDCA 本線で書き直し
- [ ] [`docs/runbook/04_検証.md`](../runbook/04_検証.md) の検証ゲートを継続改善サイクル完走基準で更新
- [ ] [`継続改善サイクル設計.md`](継続改善サイクル設計.md) / [`正解データ反映計画.md`](正解データ反映計画.md) / [`APIエンドポイント再設計案.md`](APIエンドポイント再設計案.md) / [`Elasticsearch-GCP稼働先比較.md`](Elasticsearch-GCP稼働先比較.md) は **設計メモとして archive** (実装が canonical に取り込まれた時点で本 docs ディレクトリから外す or `docs/decisions/` 経由で ADR 化)

**完了条件**: `tasks/TASKS_ROADMAP.md` の「今の課題」5 件がすべて解消され、本 doc の記述と canonical docs (01 / 03 / runbook) が一致。

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

---

## §5. マイルストーン

| ID | フェーズ | 状態 | メモ |
|---|---|---|---|
| M-Pivot | Phase 形式廃止 + docs 撤去 | ✅ | README / CLAUDE / AGENTS / docs/architecture/01,03 から Phase 概念撤去完了 (2026-05-06) |
| M-Wave0 | Makefile 止血 | ⏳ | 多行 shell ブロックの scripts/ 移送 |
| M-Wave1 | API 4 軸再設計 | ⏳ | `/api/v1/` `/ops/` `/ui/` `/` |
| M-Wave2 | 正解データ仕様確定 | ⏳ | Event schema + 重み付き label + synthetic |
| M-Wave3 | アプリ側 正解データログ実装 | ⏳ | EventWriter Port + Cloud Logging adapter |
| M-Wave4 | LightGBM 接続死守ライン | ⏳ | `pipeline/training_job/main.py` 配線実装 |
| M-Wave5 | 継続改善サイクル MVP | ⏳ | Composer DAG 3 本完走 + KServe 反映 |
| M-Wave6 | Elasticsearch 移行 (GKE 上) | ⏳ | ECK + LexicalSearchPort adapter swap |
| M-Wave7 | Makefile 本格整理 | ⏳ | 仕様確定後の構造的整理 |
| M-Wave8 | ドキュメント再統合 | ⏳ | canonical docs と Wave 成果の同期 |

---

## §6. 関連ドキュメント

### §6.1 設計メモ (Wave で消化される)

- [`継続改善サイクル設計.md`](継続改善サイクル設計.md) — 行動ログ → 正解データ → 継続改善サイクルの全体方針 (Wave 2-5 の母艦)
- [`正解データ反映計画.md`](正解データ反映計画.md) — 正解データ + 再学習を canonical に反映する計画 (Wave 3-5 の詳細)
- [`APIエンドポイント再設計案.md`](APIエンドポイント再設計案.md) — `/api/v1` `/ops` `/ui` 4 軸分離の再設計案 (Wave 1 の詳細)
- [`Elasticsearch-GCP稼働先比較.md`](Elasticsearch-GCP稼働先比較.md) — Cloud Run vs GKE Autopilot vs ECK の比較 (Wave 6 の判断材料)
- [`Makefile-多行禁止違反メモ.md`](Makefile-多行禁止違反メモ.md) — Makefile 内多行禁止の指摘メモ (Wave 0 / Wave 7 の起点)
- [`ルート昇格-実行メモ.md`](ルート昇格-実行メモ.md) — repo ルート昇格の実行メモ (M-Pivot で消化済、参考のみ)

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
