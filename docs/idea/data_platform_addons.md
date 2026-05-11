# 04_Data Platform Add-ons 設計

## 1. 結論

本プロジェクトでは、BigQuery を既存 DWH / operational canonical store として残しつつ、Databricks および Snowflake を外部データ基盤アドオンとして接続する。

BigQuery を Databricks / Snowflake に単純置換するのではなく、以下の構成を基本方針とする。

```text
App / Search API / Feedback API
        ↓
Event Writer / Pub/Sub
        ↓
BigQuery canonical tables
        ↓
GCS Parquet export
        ↓
Data Platform Adapter
        ├─ Databricks Add-on
        └─ Snowflake Add-on
```

この構成により、既存の GCP / BigQuery / Vertex AI / Composer / GKE / KServe / Elasticsearch による MLOps 基盤を壊さず、Databricks や Snowflake へ段階的に統合できる設計を示す。

---

## 2. 目的

本アドオンの目的は、Databricks や Snowflake を主役にした別システムを作ることではない。

目的は以下である。

1. 既存 BigQuery 基盤に集約された行動ログ・正解データ・特徴量・評価指標を、外部データ基盤へ接続できることを示す
2. Databricks 統合を進める組織に対して、既存 DWH / GCP 基盤から Lakehouse へ橋渡しできる設計力を示す
3. Snowflake 統合を進める組織に対して、既存 DWH から Enterprise DWH / Governance 基盤へ接続できる設計力を示す
4. BigQuery / Databricks / Snowflake の責務分担を明確化し、単純置換ではなく段階的統合を前提としたアーキテクチャを提示する
5. MLOps 基盤における正解データ、特徴量、評価指標の portability を高める

---

## 3. 前提

本プロジェクトでは、BigQuery に以下のような canonical tables が存在する前提とする。

```text
mlops.search_events
mlops.search_impressions
mlops.user_actions
mlops.ranking_labels
mlops.evaluation_metrics
mlops.ranking_log
mlops.feedback_events
feature_mart.property_features_daily
feature_mart.property_embeddings
```

これらのテーブルは、検索ログ、ユーザー行動、正解データ、特徴量、評価指標、埋め込みデータの正本として扱う。

Databricks / Snowflake は、初期段階では本番検索・推論・再学習の必須経路には入れない。

あくまで optional add-on として、BigQuery のデータを外部データ基盤へ連携し、分析・データ加工・集約 mart 化・ガバナンス確認・DWH 統合の観点を検証する（ML 本体は GCP 側 Vertex AI / KServe に残し、外部に持ち出すのはデータだけ）。

---

## 4. 設計方針

### 4.1 BigQuery は残す

BigQuery は以下の責務を持つ。

| 領域        | 役割                                                |
| --------- | ------------------------------------------------- |
| 行動ログ      | search / impression / feedback / user action の受け皿 |
| 正解データ     | ranking_labels の正本                                |
| 特徴量       | feature_mart 系テーブルの正本                             |
| 評価指標      | evaluation_metrics の保存先                           |
| GCP MLOps | Vertex AI / Composer / KServe / GKE との接続点         |
| 監査・再現性    | 既存 pipeline / parity test / runbook の基準           |

BigQuery を消すと、既存の GCP MLOps 基盤、検証資産、Terraform / parity test / run-all-core の価値が崩れる。

そのため、BigQuery は「既存 DWH 正本」または「operational canonical store」として残す。

---

### 4.2 Databricks は Lakehouse / Unity Catalog（データ集約）アドオン

Databricks は以下の責務を持つ。

| 領域                  | 役割                             |
| ------------------- | ------------------------------ |
| Lakehouse           | Bronze / Silver / Gold レイヤーの実装 |
| データ加工・集約    | BigQuery 由来のログ・正解データ・特徴量を Silver / Gold(集約 mart) に整形・集約 |
| Notebook            | 分析・探索・業務利用サンプル                 |
| Unity Catalog 想定    | 権限・lineage・ガバナンス設計の説明対象        |

Databricks でも ML 本体は作らない（ML は GCP 側 Vertex AI / KServe に残す）。本番 pipeline を完全再構築しない。

最初に実装すべきことは、BigQuery から GCS Parquet 経由で Databricks にデータを流し、Bronze / Silver / Gold(集約 mart) の medallion 構造と parity check を示すことである。ML 本体は GCP 側（Vertex AI / KServe）に残す。

---

### 4.3 Snowflake は Enterprise DWH / Governance アドオン

Snowflake は以下の責務を持つ。

| 領域             | 役割                                   |
| -------------- | ------------------------------------ |
| Enterprise DWH | 部門横断の分析 mart 作成                      |
| BI / Reporting | 集計・分析・共有用 mart                       |
| Governance     | RBAC / schema contract / audit の説明対象 |
| Data Sharing   | 将来的な部門間・ベンダー間共有の説明対象                 |
| DWH 統合         | BigQuery 由来データを Snowflake 側へ移す検証     |

Snowflake では、ML 本体を重く作らない。

最初に実装すべきことは、GCS Parquet を Snowflake External Stage から取り込み、raw table / mart table / parity check を示すことである。

---

## 5. 全体アーキテクチャ

```text
[Search API / Feedback API]
        ↓
[Event Writer]
        ↓
[Pub/Sub]
        ↓
[BigQuery canonical tables]
        ├─ mlops.user_actions
        ├─ mlops.ranking_labels
        ├─ mlops.evaluation_metrics
        ├─ feature_mart.property_features_daily
        └─ feature_mart.property_embeddings
        ↓
[GCS Parquet Export]
        ↓
[Data Platform Adapter]
        ├─ Databricks
        │    ├─ Bronze import (生)
        │    ├─ Silver clean (conformed)
        │    └─ Gold marts (集約・分析)
        │
        └─ Snowflake
             ├─ External Stage
             ├─ COPY INTO
             ├─ Raw tables
             └─ Mart tables
```

---

## 6. 共通データ連携パターン

Databricks と Snowflake の共通部分は以下である。

```text
BigQuery
  ↓
GCS Parquet Export
  ↓
Manifest / Metadata
  ↓
External Data Platform Import
  ↓
Count / Schema / Metric Parity Check
```

共通化すべき実装は、Databricks / Snowflake 個別処理ではなく、BigQuery から GCS Parquet へ切り出す部分である。

---

## 7. 連携対象テーブル

初期実装では、すべての BigQuery テーブルを対象にしない。

最小対象は以下の 3 系統とする。

| テーブル                                   | 用途        | 優先度 |
| -------------------------------------- | --------- | --- |
| `mlops.user_actions`                   | 行動ログ      | 高   |
| `mlops.ranking_labels`                 | 正解データ     | 高   |
| `feature_mart.property_features_daily` | 特徴量       | 高   |
| `mlops.evaluation_metrics`             | 評価指標      | 中   |
| `feature_mart.property_embeddings`     | embedding | 中   |

初期実装では、`user_actions`、`ranking_labels`、`property_features_daily` を優先する。

理由は、行動ログ → 正解データ → 特徴量生成という MLOps の中核を示せるためである。

---

## 8. Databricks Add-on

### 8.1 目的

Databricks Add-on の目的は、既存 BigQuery 基盤のデータを Databricks (Lakehouse / Unity Catalog) の medallion (Bronze / Silver / Gold) + 集約 mart へ接続することである。ML はやらない（GCP 側に残す）。

### 8.2 最小構成

```text
GCS Parquet
  ↓
Databricks Bronze tables (生)
  ↓
Silver cleaned tables (conformed)
  ↓
Gold marts (集約・分析)
  ↓
Parity check (BQ ↔ Databricks)
```

### 8.3 実装対象

| 対象            | 内容                             |
| ------------- | ------------------------------ |
| Bronze import | GCS Parquet を読み込む              |
| Silver clean  | 型、欠損、重複、日付を整える                 |
| Gold marts    | 集約・分析 mart を作る (label distribution / feature summary / daily action counts 等) |
| Parity check  | BigQuery 側との件数・schema・主要指標を比較  |

### 8.4 やらないこと

初期段階では以下はやらない。

* Databricks Workflows で全 pipeline を再構築する
* Vertex AI Pipelines を Databricks に置換する
* KServe / Vertex serving を Databricks Model Serving に置換する
* BigQuery を廃止する
* Databricks Feature Store を本格導入する
* Databricks 側で ML / MLflow / training run を作る（ML は GCP 側 Vertex AI Pipelines / KServe に残す）

---

## 9. Snowflake Add-on

### 9.1 目的

Snowflake Add-on の目的は、既存 BigQuery 基盤のデータを Enterprise DWH / Governance / BI mart へ接続することである。

### 9.2 最小構成

```text
GCS Parquet
  ↓
Snowflake External Stage
  ↓
COPY INTO raw tables
  ↓
Mart tables
  ↓
Parity check
```

### 9.3 実装対象

| 対象             | 内容                            |
| -------------- | ----------------------------- |
| External Stage | GCS 上の Parquet を参照            |
| File Format    | Parquet 用 file format 定義      |
| Raw table      | 取り込み先 raw table               |
| COPY INTO      | GCS から Snowflake へ load       |
| Mart table     | 分析用 mart を作成                  |
| Parity check   | BigQuery 側との件数・schema・主要指標を比較 |

### 9.4 やらないこと

初期段階では以下はやらない。

* BigQuery を Snowflake に完全置換する
* Snowpark ML を本格導入する
* Snowflake を本番 serving 経路に入れる
* すべての feature_mart を Snowflake 側へ移す

---

## 10. 責務分担

| 層            | 役割                                                  |
| ------------ | --------------------------------------------------- |
| App / API    | 検索、feedback、行動ログ発生源                                 |
| Pub/Sub      | イベント配送                                              |
| BigQuery     | 既存 DWH 正本、行動ログ、正解データ、特徴量、評価指標                       |
| GCS          | Parquet export / platform 間受け渡し                     |
| Databricks   | Lakehouse (medallion)、データ加工・集約、Unity Catalog、Notebook       |
| Snowflake    | Enterprise DWH、BI mart、Governance、Data Sharing      |
| Vertex AI    | Pipeline、Model Registry、Feature Store、Vector Search |
| GKE / KServe | 推論 serving                                          |
| Composer     | GCP 側 orchestration                                 |
| Makefile     | 再現性ある実行・検証 target                                   |

---

## 11. 推奨ディレクトリ構成

```text
.
├── scripts/
│   ├── data_platform/
│   │   ├── export_bq_to_gcs.py
│   │   ├── manifest_build.py
│   │   └── parity_check.py
│   │
│   ├── databricks/
│   │   └── submit_job.py        # Workflows job を run-now + poll (parity は scripts/data_platform/parity_check.py 共通)
│   │
│   └── snowflake/
│       ├── load_from_gcs.sql
│       ├── validate_counts.sql
│       └── validate_schema.sql
│
├── databricks/
│   ├── notebooks/
│   │   ├── 01_bronze_import.py
│   │   ├── 02_silver_clean.py
│   │   └── 03_gold_marts.py
│   └── jobs/
│       └── data_aggregation_job.yml
│
├── snowflake/
│   ├── sql/
│   │   ├── 01_create_stage.sql
│   │   ├── 02_create_raw_tables.sql
│   │   ├── 03_copy_into.sql
│   │   └── 04_create_marts.sql
│   └── README.md
│
└── docs/
    └── architecture/
        └── 04_data_platform_addons.md
```

---

## 12. Make target 案

```makefile
data-platform-export

databricks-smoke
databricks-parity

snowflake-smoke
snowflake-parity
```

### 12.1 `data-platform-export`

BigQuery の対象テーブルを GCS Parquet に export する。

### 12.2 `databricks-smoke`

GCS Parquet を Databricks に読み込み、Bronze / Silver / Gold の最小処理を実行する。

### 12.3 `databricks-parity`

Databricks 側の count / schema / key metrics を BigQuery 側と比較する。

### 12.4 `snowflake-smoke`

GCS Parquet を Snowflake External Stage 経由で取り込み、raw / mart table を作成する。

### 12.5 `snowflake-parity`

Snowflake 側の count / schema / key metrics を BigQuery 側と比較する。

---

## 13. `run-all-core` との関係

Databricks / Snowflake は初期段階では `run-all-core` に含めない。

理由は以下である。

1. 既存の GCP MLOps 本線を壊さないため
2. Databricks / Snowflake は optional add-on であるため
3. 外部サービスの状態により core validation が不安定化するのを避けるため
4. 教材として、本線と外部基盤連携を分離した方が理解しやすいため

将来的に安定したら、以下のような optional validation として追加する。

```text
make run-all-core
make data-platform-export
make databricks-parity
make snowflake-parity
```

---

## 14. Parity Check 方針

Databricks / Snowflake で最も重要なのは、派手な処理ではなく parity check である。

確認対象は以下。

| 観点                 | 内容                          |
| ------------------ | --------------------------- |
| row count          | BigQuery と外部基盤の件数一致         |
| schema             | カラム名・型の一致または許容差分            |
| null ratio         | 主要カラムの null 比率              |
| label distribution | `ranking_labels` の label 分布 |
| date range         | 対象期間の一致                     |
| key uniqueness     | 主キー・疑似主キーの重複確認              |
| metric parity      | 集計値・評価指標の一致                 |

これにより、単なるデータ転送ではなく、移行・統合・監査に耐える接続であることを示す。

---

## 15. キャリア訴求ポイント

このアドオンにより、以下を説明できる。

```text
GCP / BigQuery / Vertex AI / Composer / GKE / KServe を使った MLOps 基盤を構築した上で、
BigQuery を既存 DWH 正本として残し、
Databricks および Snowflake に接続できる Data Platform Adapter 設計へ拡張した。
```

Databricks 向けには、以下を訴求する。

```text
既存 BigQuery 基盤の行動ログ・正解データ・特徴量を、
GCS Parquet 経由で Databricks に取り込み、
Bronze / Silver / Gold の medallion 構造と集約 mart に接続できる（ML 本体は GCP 側 Vertex AI / KServe に残す）。
```

Snowflake 向けには、以下を訴求する。

```text
既存 BigQuery 基盤の行動ログ・正解データ・特徴量を、
GCS Parquet 経由で Snowflake に取り込み、
Enterprise DWH / BI mart / Governance の検証に接続できる。
```

---

## 16. 破綻条件

この設計が弱くなる条件は以下である。

1. BigQuery と Databricks / Snowflake の責務分担が曖昧になる
2. BigQuery を廃止するように見せてしまい、既存 GCP MLOps 基盤の価値が消える
3. Databricks と Snowflake を同じものとして説明してしまう
4. 接続だけで終わり、parity check がない
5. Databricks 側で Bronze / Silver / Gold(集約 mart) の最低限の処理がない
6. Snowflake 側で Stage / COPY INTO / Mart / validation の最低限の処理がない
7. `run-all-core` に混ぜて、本線の安定性を落とす
8. Databricks 側で ML をやり始めて Snowflake と非対称になる / GCP 側 ML と二重管理になる（ML は GCP 側 Vertex AI / KServe に残す）

---

## 17. 実装スコープ

### M-Wave10: Data Platform Add-ons

| ID  | 内容                                      | 優先度 |
| --- | --------------------------------------- | --- |
| 10A | BigQuery → GCS Parquet Export           | 高   |
| 10B | Export manifest / metadata              | 高   |
| 10C | Databricks Bronze / Silver / Gold smoke | 高   |
| 10E | Snowflake Stage / COPY INTO smoke       | 高   |
| 10F | Snowflake mart smoke                    | 中   |
| 10G | Databricks parity check                 | 高   |
| 10H | Snowflake parity check                  | 高   |
| 10I | Docs / runbook / architecture update    | 高   |

> 旧 `10D Databricks MLflow train smoke` は削除 — **Databricks 側で ML はやらない**（ML は GCP 側 Vertex AI Pipelines / KServe に残す）。10E〜10I の ID はそのまま。

---

## 18. 最小完成条件

M-Wave10 の最小完成条件は以下。

1. BigQuery から対象テーブルを GCS Parquet に export できる
2. export manifest に対象テーブル、期間、件数、GCS path が記録される
3. Databricks が Parquet を読み込み、Bronze / Silver / Gold の最小処理を実行できる
4. Snowflake が Parquet を External Stage から取り込み、raw / mart table を作成できる
5. BigQuery と Databricks の row count / schema parity を確認できる
6. BigQuery と Snowflake の row count / schema parity を確認できる
7. 既存 `run-all-core` は変更しない
8. ドキュメント上で BigQuery / Databricks(Lakehouse) / Snowflake(Enterprise DWH) の責務分担が説明されている
9. Databricks 側に ML / MLflow / training は作らない（ML は GCP 側に残す）

---

## 19. 最終判断

本アドオンの主眼は、Databricks や Snowflake を重く作り込むことではない。

主眼は、既存の GCP / BigQuery MLOps 基盤を、外部データ基盤に接続できる構造にすることである。

したがって、最重要実装は以下である。

```text
BigQuery → GCS Parquet Export
Data Platform Adapter
Parity Check
```

Databricks と Snowflake は、この共通出口の接続先として扱う。

これにより、本プロジェクトは単なる GCP MLOps 教材ではなく、Databricks / Snowflake 統合にも対応できる Enterprise Data Platform / MLOps ポートフォリオとなる。
