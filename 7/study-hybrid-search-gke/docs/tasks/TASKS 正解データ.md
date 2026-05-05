# Phase 7 正解データ反映計画

Phase 3 で完了した **「ML 連動検索アプリ + 正解データ作成 + 再学習」** を、Phase 7 canonical 実装へ反映するための調査結果と作業計画。

---

## 0. この計画の目的

Phase 3 では、次が **実装済みかつ `make verify-all` で検証済み**。

- `/search` → `search_events` / `search_impressions` 記録
- `/feedback` → `user_actions` 記録
- `make label` → `ranking_labels`
- `make build-training-dataset` → `training_dataset.csv`
- `make train` → `ranking_labels` 実データで LightGBM 再学習

Phase 7 でも同じ考え方を本線へ反映し、最終的に:

```text
search-api
  -> event schema
  -> ranking_labels
  -> training_dataset
  -> Vertex retrain
  -> evaluation_metrics
  -> deployment gate
  -> KServe 反映
```

を **コードと検証で成立** させる。

---

## 1. 調査結論

## 1.1 一言でいうと

**Phase 7 は docs では新 event schema / ranking_labels 経路を前提にしているが、実コードはまだ `feedback_events` 中心の旧経路が残っている。**

つまり、Phase 3 の成果を持ち上げる時の主作業は **「Phase 7 docs の想定へ実コードを追いつかせること」**。

## 1.2 いま実際に残っている旧経路

### app / API

- [`app/schemas/search.py`](../../app/schemas/search.py)
  - `FeedbackRequest.action` はまだ `click|favorite|inquiry`
- [`app/api/routers/feedback_router.py`](../../app/api/routers/feedback_router.py)
  - `/feedback` は旧 action 前提
- [`app/services/feedback_service.py`](../../app/services/feedback_service.py)
  - `FeedbackRecorder` 1 本だけ
- [`app/container/infra.py`](../../app/container/infra.py)
  - `PubSubFeedbackRecorder` を組んでいる
- [`app/services/search_service.py`](../../app/services/search_service.py)
  - `EventWriter` 未接続、`ranking_log_publisher` のみ

### 学習データ / trainer

- [`ml/data/loaders/ranker_repository.py`](../../ml/data/loaders/ranker_repository.py)
  - `ranking_log × feedback_events` join で label を作る旧設計
- [`pipeline/training_job/main.py`](../../pipeline/training_job/main.py)
  - TODO が残っており、**BigQuery loader は実装済みでも KFP component 側が未配線**
- [`pipeline/training_job/components/load_features.py`](../../pipeline/training_job/components/load_features.py)
  - docs コメントどおり contract stub のまま

### infra / BigQuery

- [`infra/terraform/modules/data/main.tf`](../../infra/terraform/modules/data/main.tf)
  - `mlops.feedback_events` はある
  - `search_events` / `search_impressions` / `user_actions` / `ranking_labels` / `evaluation_metrics` の canonical 一式にコード側がまだ追従していない
- [`tests/integration/infra/test_infra_ranker_tables.py`](../../tests/integration/infra/test_infra_ranker_tables.py)
  - `feedback_events` 中心の構造検証

### UI

- [`app/api/routers/ui_router.py`](../../app/api/routers/ui_router.py)
  - `/ui/dev` `/ui/dev/model/metrics` `/ui/dev/data` `/ui/dev/ops` はある
  - ただし **Phase 3 の物件詳細ページ `/ui/property/{property_id}` は未実装**
- `/admin/mlops`
  - 調査範囲では未実装

## 1.3 docs が先行している箇所

- [`docs/architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
  - `EventWriter` / `EventRepository` / `LabelRepository` / `TrainingDatasetRepository` / `MetricsRepository`
  - `search_events` / `search_impressions` / `user_actions` / `ranking_labels`
  - `FeedbackRequest.action` 5 種
  - `ranking_labels -> training_dataset -> Composer DAG`

つまり **設計書の方向は正しい**。問題は **実コードがそこまで追従していない** 点。

---

## 2. 方針

## 2.1 基本方針

Phase 3 と同様、**app 層の contract を先に固め、保存先や orchestration は adapter 差し替えで吸収する**。

守ること:

- `app/` 配下の contract は Phase 3 と極力同型にする
- 旧 `feedback_events` 直結の学習経路は段階的に撤去する
- Phase 7 では最終的に `/admin/mlops` を 1 ページだけ追加する

## 2.2 実装順序

依存関係の都合で、次の順で進める。

1. app / API contract
2. event schema / BigQuery / Terraform
3. repository / labeling / dataset / metrics
4. KFP / Composer 本線
5. UI / `/admin/mlops`
6. tests / docs / runbook

---

## 3. 作業計画

## 3.1 Wave A — app contract を Phase 3 と揃える

**目的**: 検索アプリが Phase 3 と同じ action / event contract で話せるようにする。

### 作業

- `FeedbackRequest.action` を 3 種から 5 種へ拡張
  - `click`
  - `detail_view`
  - `favorite`
  - `request_button_click`
  - `request_complete`
- `FeedbackService` を `FeedbackRecorder` 単独から、Phase 3 と同様に
  - legacy 互換 recorder
  - event writer
  の二経路へ拡張
- `SearchService` から `EventWriter.emit_search_event(...)` / `emit_impression(...)` を呼べるようにする
- `/feedback` から `EventWriter.emit_user_action(...)` を呼べるようにする
- **アプリ取得不可 4 種** は引き続き UI / API では受けない
  - `inquiry_complete`
  - `contract`
  - `bounce`
  - 長時間滞在

### 対象候補

- [`app/schemas/search.py`](../../app/schemas/search.py)
- [`app/services/feedback_service.py`](../../app/services/feedback_service.py)
- [`app/services/search_service.py`](../../app/services/search_service.py)
- [`app/api/routers/feedback_router.py`](../../app/api/routers/feedback_router.py)
- [`app/composition_root.py`](../../app/composition_root.py)
- [`app/container/infra.py`](../../app/container/infra.py)
- `app/services/protocols/` 新規追加
  - `event_writer.py`
  - `event_repository.py`
  - `label_repository.py`
  - 必要なら `training_dataset_repository.py`
  - 必要なら `metrics_repository.py`

### 完了条件

- `/feedback` が 5 種 action を受ける
- `/search` と `/feedback` から event schema へ publish できる
- 旧 `feedback_events` best-effort publish は互換目的で当面残してよい

---

## 3.2 Wave B — BigQuery event schema を本当に作る

**目的**: docs に書かれている canonical event schema を Terraform と実テーブルで成立させる。

### 作業

- `mlops.feedback_events` 依存のままではなく、以下を追加
  - `mlops.search_events`
  - `mlops.search_impressions`
  - `mlops.user_actions`
  - `mlops.ranking_labels`
  - `mlops.evaluation_metrics`
- 必要なら raw / curated 経路の dataset / table 命名を整理
- BigQuery Subscription / Cloud Logging sink / Eventarc のどこで何を受けるかを明示

### 対象候補

- [`infra/terraform/modules/data/main.tf`](../../infra/terraform/modules/data/main.tf)
- [`infra/terraform/modules/messaging/`](../../infra/terraform/modules/messaging)
- `infra/sql/` または `definitions/` 配下の event/label SQL 置き場
- [`tests/integration/infra/test_infra_ranker_tables.py`](../../tests/integration/infra/test_infra_ranker_tables.py)

### 完了条件

- Terraform で event schema 4 テーブル以上が宣言される
- 旧 `feedback_events` の位置付けが
  - 互換残置
  - または完全撤去
  のどちらかで明確になる

---

## 3.3 Wave C — repository を `feedback_events` 依存から `ranking_labels` 依存へ切り替える

**目的**: trainer が本当に正解データを見る状態にする。

### 作業

- `BigQueryRankerRepository` を作り直す
  - 旧: `ranking_log × feedback_events`
  - 新: `ranking_labels × search_impressions × feature mart`
- label 列は `relevance_label` 相当の意味へ寄せる
- 旧 inquiry/favorite/click の CASE label は撤去
- `evaluation_metrics` の保存先 repository も用意する

### 対象候補

- [`ml/data/loaders/ranker_repository.py`](../../ml/data/loaders/ranker_repository.py)
- `ml/data/loaders/bigquery_ranker_repository.py` に分離する案も可
- `ml/data/feature_engineering/`

### 完了条件

- `fetch_training_rows()` が `ranking_labels` ベースになる
- trainer が `feedback_events` ではなく `ranking_labels` を前提にする

---

## 3.4 Wave D — labeling / dataset / metrics の job を実装する

**目的**: Phase 3 の `make label` / `make build-training-dataset` / `make evaluate` 相当を、Phase 7 の BigQuery/GCS 版で成立させる。

### 作業

- BigQuery labeling 実装
  - `search_impressions × user_actions`
  - 重み付き relevance
  - synthetic 注入
- training dataset 生成
  - `ranking_labels × feature mart × search_impressions`
- evaluation metrics 生成
  - `ndcg_at_10`
  - `map`
  - `recall_at_20`
  - 可能なら `ctr` / `cvr`

### 対象候補

- `pipeline/labeling_job/` 新設
- `pipeline/training_dataset_job/` 新設
- `pipeline/evaluation_job/` 追加または既存 `components/evaluate.py` 再編
- `definitions/labeling/synthetic_actions.yaml` を Phase 3 から持ち込む
- Phase 4 / 7 共通にしたい純粋ロジックは `ml/labeling/` へ

### 完了条件

- `ranking_labels` が生成される
- `training_dataset` が GCS または artifact として保存される
- `evaluation_metrics` が BigQuery に保存される

---

## 3.5 Wave E — KFP / Composer 本線へ実データを通す

**目的**: docs に書いてある `retrain_orchestration` を本当に正解データ駆動にする。

### 作業

- `pipeline/training_job/components/load_features.py` の contract stub 撤去
- `BigQueryRankerRepository` を component 内から実呼び出し
- training frame を parquet 等で受け渡し
- `train_reranker.py` が `df=None` fallback に落ちないようにする
- Composer DAG `retrain_orchestration` から
  - labeling
  - dataset
  - retrain
  - evaluate
  - promote 判定
  の順序を確認・修正

### 対象候補

- [`pipeline/training_job/main.py`](../../pipeline/training_job/main.py)
- `pipeline/training_job/components/load_features.py`
- `pipeline/training_job/components/train_reranker.py`
- [`pipeline/dags/retrain_orchestration.py`](../../pipeline/dags/retrain_orchestration.py)

### 完了条件

- Vertex retrain が `ranking_labels` 由来の dataset を実際に consume する
- docs の「stub 残り」が消える

---

## 3.6 Wave F — Phase 7 UI / `/admin/mlops` を追加する

**目的**: 将来展開どおり、Phase 7 にだけ `/admin/mlops` 1 ページを持たせる。

### 作業

- 既存 `/ui/dev/model/metrics` と `/ui/dev/data` は維持
- `/admin/mlops` 追加
  - ログ件数
  - label 作成状況
  - dataset 作成状況
  - 評価指標
  - deployment gate 結果
  - 現行モデル情報
- 必要なら `/ui/property/{property_id}` も Phase 3 から移植
  - ただし優先度は `/admin/mlops` より低い

### 対象候補

- [`app/api/routers/ui_router.py`](../../app/api/routers/ui_router.py)
- `app/api/routers/admin_router.py` 新設案
- `app/templates/`
- `app/static/js/`

### 完了条件

- `/admin/mlops` から Phase 7 の継続改善サイクルの状態が見える

---

## 3.7 Wave G — テスト / contract / docs を新 canonical に揃える

**目的**: docs だけ先行している状態を終わらせ、壊れたら test が止めるようにする。

### 作業

- app contract test 更新
  - `/feedback` action 5 種
- infra contract test 更新
  - event schema 新テーブル
- workflow contract test 更新
  - `ranking_labels -> training_dataset -> retrain_orchestration`
- docs 更新
  - `01_仕様と設計.md`
  - `03_実装カタログ.md`
  - `04_検証.md`
  - `05_運用.md`
  - `TASKS_ROADMAP.md`

### 完了条件

- docs とコードが同じことを言っている
- 新 event schema / label flow を test が固定している

---

## 4. 推奨実施順

実装順は次を推奨する。

1. Wave A: app contract
2. Wave B: BigQuery schema
3. Wave C: repository 切り替え
4. Wave D: labeling / dataset / metrics jobs
5. Wave E: KFP / Composer 配線
6. Wave G: tests / docs
7. Wave F: `/admin/mlops`

理由:

- app contract と schema が固まらないと downstream が全部揺れる
- `/admin/mlops` は最後でもよいが、上流データが揃わないと空画面になる

---

## 5. リスクと注意点

## 5.1 docs 先行の罠

Phase 7 は docs がかなり先に進んでいるため、**「もう実装済みだと思い込む」事故**が起こりやすい。  
特に次は **docs 済みだがコード未追従** とみなして進める。

- `EventWriter`
- `EventRepository`
- `LabelRepository`
- `ranking_labels` 本線
- `training_dataset`
- `evaluation_metrics`

## 5.2 旧 `feedback_events` の扱い

いきなり消すと live 運用系 `ops-feedback` や既存 BigQuery Subscription が壊れる可能性がある。  
そのため移行は 2 段階にする。

1. dual-write
2. dual-read 解消
3. 旧経路削除

## 5.3 KFP / Composer は最後に壊れやすい

app と infra を先に直し、KFP component stub を最後に配線するのが安全。  
ここを先に触ると、BigQuery schema 未整備で壊れやすい。

---

## 6. マイルストーン定義

### M1: app/data contract 移行完了

- `/feedback` 5 種 action
- `search_events` / `search_impressions` / `user_actions` / `ranking_labels` テーブル定義あり
- repository が `ranking_labels` ベース

### M2: offline 正解データ経路完了

- labeling job
- dataset job
- evaluation metrics
- offline tests PASS

### M3: orchestration 本線完了

- KFP stub 撤去
- Composer retrain_orchestration が `ranking_labels` 由来で回る

### M4: operator UX 完了

- `/admin/mlops` 表示
- runbook / docs / contract test 同期

---

## 7. 最初の着手単位

最初の PR / 作業単位は次がよい。

### PR-1

**Phase 7 app contract を Phase 3 と揃える**

含めるもの:

- `FeedbackRequest.action` 5 種化
- `EventWriter` protocol と noop / adapter 導入
- `/search` / `/feedback` から event schema publish の雛形
- test 更新

理由:

- ここが全部の出発点
- BigQuery schema と job 実装を後続 PR に安全に分けられる

### PR-2

**BigQuery schema + repository 切り替え**

### PR-3

**labeling / dataset / metrics jobs**

### PR-4

**KFP / Composer 本線**

### PR-5

**`/admin/mlops` + docs 同期**

---

## 8. 参考

- [`../../../../README.md`](../../../../README.md)
- [`../../../../docs/tasks/02_移行ロードマップ.md`](../../../../docs/tasks/02_移行ロードマップ.md)
- [`../../../../3/study-hybrid-search-local/docs/architecture/01_仕様と設計.md`](../../../../3/study-hybrid-search-local/docs/architecture/01_仕様と設計.md)
- [`../../../../3/study-hybrid-search-local/docs/architecture/03_実装カタログ.md`](../../../../3/study-hybrid-search-local/docs/architecture/03_実装カタログ.md)
- [`../../../../3/study-hybrid-search-local/docs/runbook/04_検証.md`](../../../../3/study-hybrid-search-local/docs/runbook/04_検証.md)
- [`../../../../3/study-hybrid-search-local/docs/runbook/05_運用.md`](../../../../3/study-hybrid-search-local/docs/runbook/05_運用.md)
- [`../architecture/01_仕様と設計.md`](../architecture/01_仕様と設計.md)
- [`../tasks/TASKS_ROADMAP.md`](./TASKS_ROADMAP.md)
