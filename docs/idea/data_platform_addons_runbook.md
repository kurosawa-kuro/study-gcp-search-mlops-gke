# Data Platform Add-ons — 作業手順書 (M-Wave10)

設計の正本は [`data_platform_addons.md`](data_platform_addons.md)。本書はその **実装作業手順**。

**目的（再確認）**: Databricks / Snowflake を「ML 基盤」として作り込むことではなく、**既存 BigQuery MLOps 基盤を外部データ集約基盤（Databricks = Lakehouse / Unity Catalog、Snowflake = Enterprise DWH / Governance）へ接続できる設計力を示す**こと。ML は GCP 側（Vertex AI Pipelines / KServe）に残したまま、データの portability だけを外部に橋渡しする。

→ **Databricks 側でも ML（MLflow / training）はやらない。** Databricks トラックは「GCS Parquet → medallion (Bronze / Silver / Gold) Delta tables + 集約 mart + parity check」の純データ集約パイプライン。Snowflake トラックと**ほぼ同形**（ingest → raw/clean/mart → parity）にし、共通の "Data Platform Adapter" パターンが Lakehouse でも Enterprise DWH でも通用することを示す。差は **技術スタック・ガバナンスモデル**（Databricks: Delta Lake / Unity Catalog / medallion / lineage、Snowflake: warehouse / RBAC / data sharing / external table）であって「片方は ML、片方は DWH」ではない。

**前提（読者側）**: Databricks の基礎（カタログ / スキーマ / テーブル / SQL / notebook、DWH としてのテーブル操作）がある。Databricks **Free Edition** ワークスペースが既に動いている（serverless + Unity Catalog 前提）。Snowflake は未契約でも Databricks トラックだけ先行できる。

**この手順の主眼**（設計 §19）: 共通出口（BQ → GCS Parquet export + parity check）を先に固め、その接続先として Databricks / Snowflake を最小構成で繋ぐ。

---

## 0. 全体の作業順（依存関係）

```text
Phase 0  scaffolding + 前提確認
   ↓
Phase 1  10A/10B: BQ → GCS Parquet export + manifest      ← 共通出口（最重要）
   ↓
Phase 2  10C: Databricks Free Edition で Bronze / Silver / Gold(集約 mart)   ← ML なし
   ↓
Phase 3  10G: Databricks parity check（BQ ↔ Databricks の count/schema/metric 一致）
   ↓
Phase 4  Make target + docs 昇格（10I）
   ↓
（並行 / 後回し可）Phase 5  10E/10F/10H: Snowflake Stage/COPY INTO/Mart + parity
```

`run-all-core` には**入れない**（設計 §13）。安定したら optional として `make data-platform-export && make databricks-parity` を別途叩く運用。

---

## Phase 0 — scaffolding + 前提確認

### 0.1 前提リソース

| 必要なもの | 確認/準備 |
|---|---|
| BigQuery canonical tables が中身入りで存在 | このリポは PDCA loop で BQ を destroy する。`make deploy-all` → `make seed-test` → `make run-all-core` 完走後に `mlops.user_actions` / `mlops.ranking_labels` / `feature_mart.property_features_daily` 等が埋まる。export 直前にこれらが空でないことを `bq query 'SELECT COUNT(*) FROM mlops.user_actions'` で確認 |
| GCS export bucket | 既存 `gs://mlops-dev-a-artifacts` 配下の `data-platform-export/` プレフィックスを使う（新 bucket を Terraform に足してもよいが学習データは ephemeral なので不要）。`destroy-all` で消える点に注意（消えたら再 export） |
| `gcloud` / `bq` 認証 | `gcloud auth list` で `mlops-dev-a` にアクセスできる状態 |
| Databricks Free Edition workspace | サインイン済。**Personal Access Token (PAT)** 発行（User Settings → Developer → Access tokens）。workspace URL を控える |
| Databricks CLI | `databricks configure --token`（host + PAT）。`DATABRICKS_HOST` / `DATABRICKS_TOKEN` 環境変数でも可 |

### 0.2 ディレクトリ作成（設計 §11 ベース、ML 関連を除いた版）

```text
scripts/data_platform/
  export_bq_to_gcs.py     # 10A: 対象 BQ table → GCS Parquet
  manifest_build.py       # 10B: export manifest (対象/期間/件数/path/schema)
  parity_check.py         # 10G/10H: BQ ↔ 外部基盤の parity（--target=databricks|snowflake）
scripts/databricks/
  submit_job.py           # 10C: Databricks Workflows job を run-now + poll
databricks/
  notebooks/
    01_bronze_import.py   # GCS Parquet → bronze Delta tables（生）
    02_silver_clean.py    # 型/欠損/重複/日付 整形 → silver
    03_gold_marts.py      # 集約・分析 mart → gold（label distribution / feature summary 等）
  jobs/
    data_aggregation_job.yml   # Workflows job (01→02→03)
snowflake/                # Phase 5
  sql/{01_create_stage.sql,02_create_raw_tables.sql,03_copy_into.sql,04_create_marts.sql}
  README.md
```

※ 設計 §11 の `04_mlflow_train_smoke.py` / `feature_engineering_job.yml` は作らない（ML をやらないため）。`03_gold_features.py` → `03_gold_marts.py` に改名（集約 mart）。Job 名も `feature_engineering_job` → `data_aggregation_job`。

### 0.3 secret 取り扱い

- Databricks PAT・GCP SA key は**コミットしない**。`~/.databrickscfg`（gitignore 配下）+ 環境変数で渡す。
- notebook に secret を直書きしない（Databricks Secrets / widgets 経由）。
- 新 export bucket を Terraform に足す場合のみ `infra/terraform/modules/data/` か新 `data_platform` module に。足さない（既存 bucket のプレフィックス利用）なら IaC 変更なし。

### 0.4 対象テーブル（設計 §7、初期は高優先 3 系統）

| BQ table | 役割 |
|---|---|
| `mlops.user_actions` | 行動ログ |
| `mlops.ranking_labels` | 正解データ |
| `feature_mart.property_features_daily` | 特徴量（日次集計） |
| （中優先、後で）`mlops.evaluation_metrics` / `feature_mart.property_embeddings` | 評価指標 / embedding |

---

## Phase 1 — 10A/10B: BigQuery → GCS Parquet export + manifest（共通出口、最重要）

### 1.1 `scripts/data_platform/export_bq_to_gcs.py`（10A）

対象 3 テーブルを `gs://mlops-dev-a-artifacts/data-platform-export/<table>/<YYYYMMDD>/part-*.parquet` に Parquet で出す。小データなので `bq extract` でよい。テーブルリストは hard-code せず module 定数 or `setting.yaml` に。`make data-platform-export` から呼ぶ。

```python
# scripts/data_platform/export_bq_to_gcs.py
EXPORT_TABLES = {
    "mlops.user_actions": "user_actions",
    "mlops.ranking_labels": "ranking_labels",
    "feature_mart.property_features_daily": "property_features_daily",
}
def main() -> int:
    project = env("PROJECT_ID"); bucket = f"{project}-artifacts"; today = date.today().strftime("%Y%m%d")
    for src, name in EXPORT_TABLES.items():
        dst = f"gs://{bucket}/data-platform-export/{name}/{today}/part-*.parquet"
        run(["bq", "extract", f"--project_id={project}", "--destination_format=PARQUET",
             "--compression=SNAPPY", f"{project}:{src}", dst], check=True)
    return 0
```

### 1.2 `scripts/data_platform/manifest_build.py`（10B）

export manifest（JSON）に **対象テーブル / 期間 / 件数 / GCS path / BQ schema** を記録 — これが Phase 3 parity の基準。出力: `gs://.../data-platform-export/_manifest/<date>.json` + `dist/data_platform/manifest_<date>.json`（ローカル、gitignore）。

```json
{
  "exported_at_utc": "...", "project_id": "mlops-dev-a",
  "tables": [{"src": "mlops.user_actions", "name": "user_actions",
              "gcs": "gs://mlops-dev-a-artifacts/data-platform-export/user_actions/20260512/",
              "row_count": 25, "date_column": null,
              "schema": [{"name": "event_id", "type": "STRING"}, ...]}]
}
```

row_count は `bq query 'SELECT COUNT(*)'`、schema は `bq show --schema --format=prettyjson`。

### 1.3 `make data-platform-export`

```makefile
data-platform-export: ## BigQuery canonical tables を GCS Parquet に export + manifest 生成
	uv run python -u -m scripts.data_platform.export_bq_to_gcs
	uv run python -u -m scripts.data_platform.manifest_build
```

### Phase 1 完了確認
- `gsutil ls gs://mlops-dev-a-artifacts/data-platform-export/` に 3 テーブル + `_manifest/<date>.json`
- manifest の row_count が `bq query 'SELECT COUNT(*)'` と一致
- `make check`: 新規 `scripts/data_platform/*.py` が ruff / format / pure-logic 単体 test を通る

---

## Phase 2 — 10C: Databricks Free Edition で Bronze / Silver / Gold（ML なし、データ集約のみ）

### 2.1 GCS → Databricks の接続（Free Edition の作法）

Databricks Free Edition は **serverless + Unity Catalog 前提**。クラスタ Spark conf に GCS SA key を直書きできないので、**Unity Catalog の Storage Credential + External Location** 経由が canonical（= Lakehouse / governance の設計力アピールにもなる）。

1. **GCP 側**: `gs://mlops-dev-a-artifacts/data-platform-export/*` を read できる service account（`roles/storage.objectViewer`、プレフィックス scope）。Databricks に渡す短命 SA key（学習用、ローテーション前提。本番は GCP↔Databricks の Workload Identity Federation）。
2. **Databricks 側**（Catalog Explorer / SQL）: **Storage credentials** に上記 SA を登録 → **External locations** に `gs://mlops-dev-a-artifacts/data-platform-export/` を紐付け。
3. 確認: SQL editor で `LIST 'gs://mlops-dev-a-artifacts/data-platform-export/'`。
   - ⚠️ region / Free Edition 制約で詰まる場合の代替: `gsutil cp -r gs://.../data-platform-export/ ./local && databricks fs cp -r ./local dbfs:/Volumes/<catalog>/<schema>/<volume>/` で UC Volume に手動ロード → notebook は Volume パスを読む（設計力アピールは落ちるが学習は進む）。

### 2.2 カタログ / スキーマ（medallion）

```sql
CREATE CATALOG IF NOT EXISTS hybrid_search;
USE CATALOG hybrid_search;
CREATE SCHEMA IF NOT EXISTS bronze;   -- 生取り込み
CREATE SCHEMA IF NOT EXISTS silver;   -- conformed / cleaned
CREATE SCHEMA IF NOT EXISTS gold;     -- 集約・分析 mart
```

### 2.3 `databricks/notebooks/01_bronze_import.py`（Bronze — 生取り込み）

GCS Parquet → bronze Delta tables（型変換しない、生）。manifest の最新 `<date>` を widget で受ける。

```python
dbutils.widgets.text("export_date", "20260512")
date = dbutils.widgets.get("export_date")
base = "gs://mlops-dev-a-artifacts/data-platform-export"
for name in ["user_actions", "ranking_labels", "property_features_daily"]:
    (spark.read.parquet(f"{base}/{name}/{date}/")
        .write.format("delta").mode("overwrite").saveAsTable(f"hybrid_search.bronze.{name}"))
display(spark.sql("SELECT COUNT(*) FROM hybrid_search.bronze.user_actions"))
```

### 2.4 `02_silver_clean.py`（Silver — conformed / cleaned）

型・欠損・重複・日付を整える DWH 的クレンジング。例: `timestamp` を `TIMESTAMP` に、`property_id` の重複除去（最新優先）、`event_date` を `DATE` に、不正値除去。`silver.{user_actions,ranking_labels,property_features_daily}` に書く。BQ 側の schema / 値とできるだけ同じになるように（parity が取りやすい）。

### 2.5 `03_gold_marts.py`（Gold — 集約・分析 mart）

「データ集約基盤としての成果物」= **集約 mart**。ML training frame ではなく、DWH / BI が出すような集計テーブル。例:

| gold table | 内容 |
|---|---|
| `gold.label_distribution` | `relevance_label` ごとの件数・比率（`ranking_labels` 集約） |
| `gold.feature_summary` | `property_id` ごとの特徴量サマリ（`AVG`/`MIN`/`MAX` ctr・fav_rate・inquiry_rate 等、`property_features_daily` 集約） |
| `gold.daily_action_counts` | `event_date` × `action_type` ごとの行動件数（`user_actions` 集約） |
| `gold.search_label_join`（任意）| `ranking_labels` × `property_features_daily` を `property_id` で join した分析用ワイドテーブル（"feature view" としての data 成果物。ML はしない） |

`gold.*` に書く。これらが Snowflake の `mart.*` と対応する（同じ集約を Lakehouse 側でも作れることを示す）。

### 2.6 `databricks/jobs/data_aggregation_job.yml`（Workflows job）

01→02→03 を直列の Workflows job として定義。`databricks bundle deploy`（Databricks Asset Bundle）or REST で workspace に登録、serverless job として実行。

### Phase 2 完了確認
- `hybrid_search.bronze.{user_actions,ranking_labels,property_features_daily}` 作成、`SELECT COUNT(*)` が export 件数と一致
- `silver.*` 作成、cleaning 後の件数・schema が想定どおり
- `gold.{label_distribution,feature_summary,daily_action_counts}` 作成、集計値が手計算 / BQ 側集計と一致
- MLflow / training run は**ない**（やらないので無いのが正しい）

---

## Phase 3 — 10G: Databricks parity check（最重要、設計 §14）

### 3.1 `scripts/data_platform/parity_check.py --target=databricks`

ローカル（このリポ）から走らせる。BQ 側は `bq query`、Databricks 側は **Databricks SQL Statement Execution API**（REST、`DATABRICKS_HOST` + `DATABRICKS_TOKEN` 認証、`databricks-sdk` or `requests`）で同クエリを `hybrid_search.bronze.*` / `silver.*` / `gold.*` に投げ、比較。

確認観点（設計 §14、ML metric は無し）:

| 観点 | クエリ | 判定 |
|---|---|---|
| row count | `SELECT COUNT(*) FROM <t>` | BQ == Databricks（完全一致） |
| schema | BQ: `bq show --schema` / DB: `DESCRIBE TABLE` | カラム名集合一致。型は許容差分（型マッピング表で正規化して比較） |
| null ratio | `SELECT COUNTIF(col IS NULL)/COUNT(*) FROM <t>`（主要カラム）| 差分 ≤ 1e-9 |
| label distribution | `SELECT relevance_label, COUNT(*) FROM ranking_labels GROUP BY 1` | 分布完全一致 |
| date range | `SELECT MIN(event_date), MAX(event_date) FROM <t>` | 一致 |
| key uniqueness | `SELECT COUNT(*) - COUNT(DISTINCT <key>) FROM <t>` | 両側とも 0（or 同値） |
| metric parity | gold の集計値（`label_distribution` の比率、`feature_summary` の AVG 等）| 差分 ≤ 1e-6 |

manifest（Phase 1 の JSON）の row_count / schema を BQ 側基準として再利用できる。型マッピング: `STRING↔string`, `INT64↔bigint`, `FLOAT64↔double`, `TIMESTAMP↔timestamp`, `DATE↔date`, `BOOL↔boolean`, `REPEATED↔array`。

### 3.2 `make databricks-smoke` / `make databricks-parity`

```makefile
databricks-smoke: ## GCS Parquet → Databricks Bronze/Silver/Gold (data_aggregation Workflows job をトリガ)
	uv run python -u -m scripts.databricks.submit_job
databricks-parity: ## BQ ↔ Databricks の count/schema/metric parity
	uv run python -u -m scripts.data_platform.parity_check --target=databricks
```

`submit_job.py` は Jobs API `jobs/run-now` を叩いて完了まで poll（`scripts/ops/vertex/pipeline_wait.py` と同パターン）。

### Phase 3 完了確認
- `make databricks-parity` exit 0、レポートに全観点 PASS
- 意図的に Databricks 側の 1 テーブルを 1 行削って parity が FAIL になることを確認（guard が効く）

---

## Phase 4 — Make target 整備 + docs 昇格（10I）

1. Makefile に追加（`run-all-core` には**入れない**、`# ----- Data Platform Add-ons (optional) -----` セクション分け）: `data-platform-export` / `databricks-smoke` / `databricks-parity` / `snowflake-smoke` / `snowflake-parity`。`docs/conventions/Makefile規約.md` 再生成。
2. `docs/idea/data_platform_addons.md` を `docs/architecture/04_data_platform_addons.md` に昇格（ML 角度を落とした版に）。本手順書も `docs/runbook/06_data_platform_addons.md` に昇格 or `docs/idea/` に残す。
3. `docs/tasks/TASKS_ROADMAP.md` §1 / §5 に「M-Wave10 Data Platform Add-ons」を追加（10D = Databricks MLflow は**外す**）。`docs/architecture/03_実装カタログ.md` §2/§3 に Data Platform 行を追加（完了後）。
4. 軽量 contract test（`tests/integration/parity/`）: 「`EXPORT_TABLES` のキーが idea doc §7 高優先 3 テーブルと一致」「Makefile に `data-platform-export` / `databricks-parity` target が存在」「`scripts/ops/run_all.py::STEPS` に Databricks/Snowflake が**入っていない**ことを assert（設計 §16-7 破綻条件 guard）」「`databricks/notebooks/` に `*mlflow*` / `*train*` notebook が**無い**ことを assert（= 'Databricks 側で ML はやらない' を pin）」。
5. `make check` 全 PASS、`make check-layers: OK`。

---

## Phase 5 — Snowflake トラック（並行 / 後回し可、10E/10F/10H）

Snowflake アカウント取得後。Phase 1 の GCS Parquet をそのまま使う（Databricks と同じ出口）。

1. `snowflake/sql/01_create_stage.sql`: GCP の Storage Integration（Snowflake → GCS）+ External Stage `@hybrid_search_stage` を `gs://mlops-dev-a-artifacts/data-platform-export/` に。
2. `02_create_raw_tables.sql`: `raw.{user_actions,ranking_labels,property_features_daily}`（Parquet schema に合わせた DDL、`VARIANT` 受けでも可）。
3. `03_copy_into.sql`: `COPY INTO raw.user_actions FROM @hybrid_search_stage/user_actions/<date>/ FILE_FORMAT = (TYPE = PARQUET)`。
4. `04_create_marts.sql`: `mart.label_distribution` / `mart.feature_summary` / `mart.daily_action_counts`（Databricks の `gold.*` と対応する集約 mart）。
5. `make snowflake-smoke`（`scripts/snowflake/` から SnowSQL or `snowflake-connector-python` で `.sql` を順次実行）/ `make snowflake-parity`（`parity_check.py --target=snowflake`、Databricks と同じ観点を Snowflake クエリで）。

設計 §9.4 の「やらないこと」を守る。Databricks と Snowflake の差は**技術スタック・ガバナンスモデル**であって ML の有無ではない（両方 ML なし）。

---

## 完了条件（設計 §18 から ML 関連を外した版）

- [ ] BigQuery から対象 3 テーブルを GCS Parquet に export できる（`make data-platform-export`）
- [ ] export manifest に 対象テーブル / 期間 / 件数 / GCS path / schema が記録される
- [ ] Databricks が Parquet を読み込み Bronze / Silver / Gold(集約 mart) の最小処理を実行できる（`make databricks-smoke`）
- [ ] BigQuery ↔ Databricks の row count / schema / metric parity を確認できる（`make databricks-parity` exit 0）
- [ ] （Snowflake 着手時）Snowflake が External Stage 経由で Parquet を取り込み raw / mart を作れる + parity 確認できる
- [ ] 既存 `run-all-core` は変更しない（contract test で pin）
- [ ] docs 上で BigQuery / Databricks(Lakehouse) / Snowflake(Enterprise DWH) の責務分担が説明されている
- [ ] Databricks 側に ML / MLflow / training は**作らない**（contract test で pin） — Databricks は「データ集約基盤としての対応」を示すスコープに限定

---

## 罠 / 注意点

| 罠 | 対策 |
|---|---|
| **BQ canonical tables が空のまま export** | `destroy-all` 後は BQ も消える。export 前に `make deploy-all` → `seed-test` → `run-all-core` 完走を確認、最低 `make seed-test` だけでも実行。manifest の row_count が 0 なら即 fail |
| **GCS export bucket が `destroy-all` で消える** | export は ephemeral 前提。Databricks/Snowflake の external table は再 export 後に再ロード。長期保持したいなら export bucket だけ `prevent_destroy` の専用 module に（VVS Index/Endpoint と同 pattern） |
| **Databricks Free Edition の compute / region 制約** | serverless のみ・compute 時間に上限。GCS からの read は cross-cloud egress（学習データは数 KB なので無視できる）。詰まったら §2.1 の UC Volume 手動 cp 代替 |
| **GCS SA key を Databricks に登録する security** | 学習用は read-only SA + 短命 key（ローテーション前提）。本番は Workload Identity Federation。key は git に絶対入れない |
| **PAT の漏洩 / 期限** | `DATABRICKS_TOKEN` 環境変数で渡す。`~/.databrickscfg` は gitignore 配下。期限切れで parity が 401 → 再発行 |
| **schema 型の名前差分で parity が誤検知** | 型マッピング表（`STRING↔string↔VARCHAR`, `INT64↔bigint↔NUMBER`, `FLOAT64↔double↔FLOAT`, `TIMESTAMP↔timestamp↔TIMESTAMP_NTZ`, `DATE↔date↔DATE`, `BOOL↔boolean↔BOOLEAN`, `REPEATED↔array↔ARRAY`）を `parity_check.py` に持って正規化してから比較 |
| **`run-all-core` に混ぜて本線を不安定化**（設計 §16-7） | 絶対に `scripts/ops/run_all.py::STEPS` に入れない。contract test で「Databricks/Snowflake target が STEPS に無い」を assert |
| **Databricks と Snowflake を「同じもの」として説明**（設計 §16-3） | Databricks = Lakehouse / Delta Lake / Unity Catalog / medallion / lineage、Snowflake = Enterprise DWH / warehouse / RBAC / data sharing / external table。データ集約のパイプライン形は同じ、ガバナンス・技術スタックが違う |
| **「Databricks 側で ML もやる」に戻ってしまう** | スコープを「データ集約基盤としての対応」に固定。`databricks/notebooks/` に `*mlflow*` / `*train*` notebook を作らない（contract test で pin）。ML は GCP 側（Vertex AI / KServe）に残す |

---

## 最短クイックスタート（Databricks トラックだけ、~半日）

```bash
# 1. BQ canonical tables を埋める（destroy 済なら deploy から）
make deploy-all && make seed-test && make run-all-core      # 既に稼働中なら make seed-test だけ

# 2. Phase 0/1 のコード（scripts/data_platform/ 3 ファイル + Makefile target）
make data-platform-export
gsutil ls -r gs://mlops-dev-a-artifacts/data-platform-export/

# 3. Databricks: Storage Credential + External Location を GCS export prefix に張る（UI）
#    → SQL editor で  LIST 'gs://mlops-dev-a-artifacts/data-platform-export/'  が叩ければ OK

# 4. databricks/notebooks/01..03 を書いて data_aggregation_job 化 → run-now（ML notebook は作らない）
make databricks-smoke

# 5. parity
make databricks-parity        # exit 0 = BQ ↔ Databricks 一致

# 6. （余裕があれば）docs 昇格 + contract test + Snowflake トラック
```

これで設計 §15 の Databricks 訴求（ML 角度を落とした版）が実物で示せる:

> 既存 BigQuery 基盤の行動ログ・正解データ・特徴量を、GCS Parquet 経由で Databricks (Lakehouse / Unity Catalog) に取り込み、Bronze / Silver / Gold の medallion 構造と集約 mart に接続できる。ML 本体は GCP 側（Vertex AI Pipelines / KServe）に残したまま、データの portability だけを外部データ集約基盤へ橋渡しした。
