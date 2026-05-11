# Data Platform Add-ons — 作業手順書 (M-Wave10)

設計の正本は [`data_platform_addons.md`](data_platform_addons.md)。本書はその **実装作業手順** — 「BigQuery canonical tables → GCS Parquet export → Databricks / Snowflake adapter → parity check」を実際にどの順で作るか。

**前提（読者側）**: Databricks の基礎（DWH としてのテーブル/カタログ操作、SQL、notebook）がある。Databricks **Free Edition** ワークスペースが既に動いている（serverless + Unity Catalog 前提の新 Free Edition）。Snowflake は未契約でも Databricks トラックだけ先行できる。

**この手順の主眼**（設計 §19 と同じ）: Databricks / Snowflake を重く作り込むことではなく、**共通出口（BQ → GCS Parquet export + parity check）を先に固め、その接続先として Databricks を最小構成で繋ぐ**こと。

---

## 0. 全体の作業順（依存関係）

```text
Phase 0  scaffolding + 前提確認            ← まずここ
   ↓
Phase 1  10A/10B: BQ → GCS Parquet export + manifest   ← 共通出口（最重要）
   ↓
Phase 2  10C/10D: Databricks Free Edition で Bronze/Silver/Gold + MLflow smoke
   ↓
Phase 3  10G: Databricks parity check（BQ ↔ Databricks の count/schema/metric 一致）
   ↓
Phase 4  Make target + docs 昇格（10I）
   ↓
（並行 / 後回し可）  Phase 5  10E/10F/10H: Snowflake Stage/COPY INTO/Mart + parity
```

`run-all-core` には**入れない**（設計 §13）。安定したら optional として `make data-platform-export && make databricks-parity` を別途叩く運用。

---

## Phase 0 — scaffolding + 前提確認

### 0.1 前提リソースを揃える

| 必要なもの | 確認/準備コマンド |
|---|---|
| BigQuery canonical tables が中身入りで存在 | このリポは PDCA loop で BQ を destroy する。`make deploy-all` → `make seed-test` → `make run-all-core` 完走後に `mlops.user_actions` / `mlops.ranking_labels` / `feature_mart.property_features_daily` 等が埋まる。export 直前にこれらが空でないことを `bq query 'SELECT COUNT(*) FROM mlops.user_actions'` 等で確認 |
| GCS export bucket | 既存の `gs://mlops-dev-a-artifacts` 配下の `data-platform-export/` プレフィックスを使う（新 bucket を Terraform に足してもよいが、学習データは ephemeral なので既存 bucket で十分）。`destroy-all` で消える点に注意（消えたら再 export） |
| `gcloud` / `bq` 認証 | `gcloud auth list` で `mlops-dev-a` にアクセスできる状態 |
| Databricks Free Edition workspace | サインイン済。**Personal Access Token (PAT)** を発行（User Settings → Developer → Access tokens）。workspace URL（`https://<...>.cloud.databricks.com` 等）を控える |
| Databricks CLI | `pip install databricks-cli`（or `databricks` v0.2x）。`databricks configure --token`（host + PAT） |

### 0.2 ディレクトリ作成（設計 §11 準拠）

```text
scripts/data_platform/
  export_bq_to_gcs.py     # 10A: 対象 BQ table → GCS Parquet
  manifest_build.py       # 10B: export manifest (対象/期間/件数/path/schema)
  parity_check.py         # 10G/10H: BQ ↔ 外部基盤の parity（--target=databricks|snowflake）
databricks/
  notebooks/
    01_bronze_import.py
    02_silver_clean.py
    03_gold_features.py
    04_mlflow_train_smoke.py
  jobs/
    feature_engineering_job.yml   # Databricks Workflows job (01→02→03→04)
snowflake/                        # Phase 5 で
  sql/{01_create_stage.sql,02_create_raw_tables.sql,03_copy_into.sql,04_create_marts.sql}
  README.md
```

`docs/architecture/04_data_platform_addons.md` は Phase 4 で `docs/idea/data_platform_addons.md` を昇格させる。

### 0.3 `.gitignore` / secret 取り扱い

- Databricks PAT・GCP SA key は **コミットしない**。`databricks configure` のローカル設定 (`~/.databrickscfg`) と環境変数で渡す（`DATABRICKS_HOST` / `DATABRICKS_TOKEN`）。
- `databricks/notebooks/*.py` は notebook source（databricks 形式 or plain .py）。secret は notebook に書かず Databricks Secrets / widgets で渡す。
- 新 export bucket を Terraform に足す場合は `infra/terraform/modules/data/` か新 `data_platform` module に。足さない場合（既存 bucket のプレフィックス利用）は IaC 変更なし。

### 0.4 対象テーブル（設計 §7、初期は高優先 3 系統）

| BQ table | 役割 | 期間 |
|---|---|---|
| `mlops.user_actions` | 行動ログ | 全件（seed は数件） |
| `mlops.ranking_labels` | 正解データ | 全件 |
| `feature_mart.property_features_daily` | 特徴量 | `event_date` 最新日（or 全件） |
| （中優先、後で）`mlops.evaluation_metrics` / `feature_mart.property_embeddings` | 評価指標 / embedding | 全件 |

---

## Phase 1 — 10A/10B: BigQuery → GCS Parquet export + manifest（共通出口）

### 1.1 `scripts/data_platform/export_bq_to_gcs.py`（10A）

やること: 対象 3 テーブルを `gs://mlops-dev-a-artifacts/data-platform-export/<table>/<YYYYMMDD>/*.parquet` に Parquet で出す。

実装方針:
- 小データなので `bq extract`（`bq extract --destination_format=PARQUET 'mlops.user_actions' 'gs://.../user_actions/<date>/*.parquet'`）が一番簡単。大きくなったら BigQuery → GCS の Export job（`google.cloud.bigquery` の `extract_table`）に。
- テーブルリストは hard-code せず `scripts/_common.py::DEFAULTS` / `env/config/setting.yaml` か module 定数で（後で増やせるように）。
- 既存 adapter 規約に合わせ `gcloud_run` ではなく `bq` を直接 `_common.run(["bq", ...])` で（`bq` は adapter 化されていない）。`scripts/adapters/` に倣うなら薄い `bq_run` を足してもよい。
- `make data-platform-export` から呼ぶ。

擬似コード:

```python
# scripts/data_platform/export_bq_to_gcs.py
EXPORT_TABLES = {
    "mlops.user_actions": "user_actions",
    "mlops.ranking_labels": "ranking_labels",
    "feature_mart.property_features_daily": "property_features_daily",
}
def main() -> int:
    project = env("PROJECT_ID"); bucket = f"{project}-artifacts"; today = date.today().strftime("%Y%m%d")
    exported = []
    for src, name in EXPORT_TABLES.items():
        dst = f"gs://{bucket}/data-platform-export/{name}/{today}/part-*.parquet"
        run(["bq", "extract", f"--project_id={project}", "--destination_format=PARQUET",
             "--compression=SNAPPY", f"{project}:{src}", dst], check=True)
        exported.append({"src": src, "name": name, "gcs": dst.replace("part-*.parquet", "")})
    # ↓ manifest_build に渡す or ここで直接書く
    return 0
```

### 1.2 `scripts/data_platform/manifest_build.py`（10B）

export manifest（JSON）に **対象テーブル / 期間 / 件数 / GCS path / BQ schema** を記録。これが Phase 3 parity の基準になる。出力先: `gs://.../data-platform-export/_manifest/<date>.json` と `dist/data_platform/manifest_<date>.json`（ローカル、gitignore）。

```json
{
  "exported_at_utc": "2026-05-12T...Z",
  "project_id": "mlops-dev-a",
  "tables": [
    {"src": "mlops.user_actions", "name": "user_actions",
     "gcs": "gs://mlops-dev-a-artifacts/data-platform-export/user_actions/20260512/",
     "row_count": 25,
     "schema": [{"name": "event_id", "type": "STRING"}, {"name": "search_id", "type": "STRING"}, ...],
     "date_column": null}
  ]
}
```

row_count は `bq query 'SELECT COUNT(*) FROM ...'`、schema は `bq show --schema --format=prettyjson 'mlops.user_actions'` から。

### 1.3 `make data-platform-export`

```makefile
data-platform-export: ## BigQuery canonical tables を GCS Parquet に export + manifest 生成
	uv run python -u -m scripts.data_platform.export_bq_to_gcs
	uv run python -u -m scripts.data_platform.manifest_build
```

### Phase 1 の完了確認
- `gsutil ls gs://mlops-dev-a-artifacts/data-platform-export/` に 3 テーブル分のディレクトリ + `_manifest/<date>.json` が出る
- manifest の row_count が `bq query 'SELECT COUNT(*)'` と一致
- `make check`: 新規 `scripts/data_platform/*.py` が ruff + `mypy --strict`（`scripts/` は mypy 対象外だが ruff/format は通す）+ pure-logic 部分の単体 test を通る

---

## Phase 2 — 10C/10D: Databricks Free Edition で Bronze/Silver/Gold + MLflow smoke

### 2.1 GCS → Databricks の接続（Free Edition の作法）

Databricks Free Edition は **serverless + Unity Catalog 前提**。クラスタの Spark conf に GCS の SA key を直書きできないので、**Unity Catalog の Storage Credential + External Location** 経由が canonical。

手順（Databricks UI / SQL）:
1. **GCP 側**: GCS bucket `mlops-dev-a-artifacts` の `data-platform-export/*` を read できる service account を作る（`roles/storage.objectViewer` をプレフィックス scope で。学習なら bucket 全体でも可）。Databricks に渡すための短命 SA key（JSON）を発行（本番なら Workload Identity Federation だが学習は key で可、ローテーション前提）。
2. **Databricks 側**: Catalog Explorer → External Data → **Storage credentials** → GCP service account の email（key を Databricks が管理する形式）を登録。→ **External locations** → `gs://mlops-dev-a-artifacts/data-platform-export/` を上記 credential に紐付け。
3. 接続確認: SQL editor で `LIST 'gs://mlops-dev-a-artifacts/data-platform-export/'` が叩ければ OK。
   - ⚠️ Free Edition がアクセスできない / region 制約で詰まる場合の代替: `gsutil cp -r gs://.../data-platform-export/ ./local && databricks fs cp -r ./local dbfs:/Volumes/<catalog>/<schema>/<volume>/` で UC Volume に手動ロード → notebook は Volume パスを読む。設計力アピールは落ちるが学習は進む。

### 2.2 カタログ / スキーマ作成（Bronze/Silver/Gold）

```sql
CREATE CATALOG IF NOT EXISTS hybrid_search;
USE CATALOG hybrid_search;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```

### 2.3 `databricks/notebooks/01_bronze_import.py`（10C — Bronze）

GCS Parquet をそのまま Bronze に取り込む（型変換しない、生）。3 テーブル分。`COPY INTO` か `CREATE TABLE ... AS SELECT * FROM parquet.\`gs://...\``。manifest の最新 `<date>` を widget で受ける。

```python
# Databricks notebook
dbutils.widgets.text("export_date", "20260512")
date = dbutils.widgets.get("export_date")
base = "gs://mlops-dev-a-artifacts/data-platform-export"
for name in ["user_actions", "ranking_labels", "property_features_daily"]:
    spark.read.parquet(f"{base}/{name}/{date}/").write.mode("overwrite").saveAsTable(f"hybrid_search.bronze.{name}")
display(spark.sql("SELECT COUNT(*) FROM hybrid_search.bronze.user_actions"))
```

### 2.4 `02_silver_clean.py`（10C — Silver）

型・欠損・重複・日付を整える。例: `timestamp` を `TIMESTAMP` に、`property_id` の重複除去（最新優先）、`event_date` を `DATE` に。`silver.*` に書く。

### 2.5 `03_gold_features.py`（10C — Gold）

学習・評価に使える特徴量 table。例: `silver.ranking_labels` × `silver.property_features_daily` を `property_id` で join した training frame（`request_id` / `property_id` / 各特徴量 / `relevance_label`）。`gold.training_frame` に書く。BQ 側の `pipeline/training_job/components/load_features.py` のクエリと**同じ列構成**にすると parity が取りやすい。

### 2.6 `04_mlflow_train_smoke.py`（10D — MLflow smoke）

`gold.training_frame` を pandas にして LightGBM LambdaRank の最小 training run を MLflow に記録。

```python
import mlflow, lightgbm as lgb
df = spark.table("hybrid_search.gold.training_frame").toPandas()
X = df.drop(columns=["relevance_label","request_id","property_id"]); y = df["relevance_label"]
group = df.groupby("request_id").size().tolist()  # LambdaRank の group
mlflow.lightgbm.autolog()
with mlflow.start_run(run_name="lgbm_lambdarank_smoke"):
    ds = lgb.Dataset(X, label=y, group=group)
    lgb.train({"objective":"lambdarank","metric":"ndcg","ndcg_eval_at":[10]}, ds, num_boost_round=10)
```

Free Edition の MLflow（managed）に run / params / metrics / model が残る。

### 2.7 `databricks/jobs/feature_engineering_job.yml`（Workflows job）

01→02→03→04 を直列の Workflows job として定義。`databricks bundle deploy`（Databricks Asset Bundle）or REST API で workspace に登録。serverless job として実行。

### Phase 2 の完了確認
- `hybrid_search.bronze.{user_actions,ranking_labels,property_features_daily}` が作成され `SELECT COUNT(*)` が export 件数と一致
- `silver.*` / `gold.training_frame` が作成され、`gold.training_frame` の行数 = `ranking_labels` の `(request_id, property_id)` ペア数
- MLflow に `lgbm_lambdarank_smoke` run（ndcg metric 付き）が記録

---

## Phase 3 — 10G: Databricks parity check（最重要、設計 §14）

### 3.1 `scripts/data_platform/parity_check.py --target=databricks`

ローカル（このリポ）から走らせる。BQ 側は `bq query`、Databricks 側は **Databricks SQL Statement Execution API**（REST、`DATABRICKS_HOST` + `DATABRICKS_TOKEN` で認証、`databricks-sdk` python lib か直接 `requests`）で同じクエリを Databricks の `hybrid_search.bronze.*` / `gold.training_frame` に投げ、結果を比較。

確認観点（設計 §14）と判定:

| 観点 | クエリ | 判定 |
|---|---|---|
| row count | `SELECT COUNT(*) FROM <t>` | BQ == Databricks（完全一致） |
| schema | BQ: `bq show --schema` / DB: `DESCRIBE TABLE` | カラム名集合一致。型は許容差分（`STRING↔string`, `INT64↔bigint`, `FLOAT64↔double`, `TIMESTAMP↔timestamp`, `DATE↔date` のマッピング表で正規化して比較） |
| null ratio | `SELECT COUNTIF(col IS NULL)/COUNT(*) FROM <t>` (主要カラム) | 差分 ≤ 1e-9（seed は決定的） |
| label distribution | `SELECT relevance_label, COUNT(*) FROM ranking_labels GROUP BY 1` | 分布完全一致 |
| date range | `SELECT MIN(event_date), MAX(event_date) FROM <t>` | 一致 |
| key uniqueness | `SELECT COUNT(*) - COUNT(DISTINCT <key>) FROM <t>` | 両側とも 0（or 同値） |
| metric parity | gold の集計値（例: `AVG`(各特徴量)）| 差分 ≤ 1e-6 |

manifest（Phase 1 で作った JSON）の row_count / schema を BQ 側の基準として使う（再クエリ不要にできる）。

### 3.2 `make databricks-smoke` / `make databricks-parity`

```makefile
databricks-smoke: ## GCS Parquet → Databricks Bronze/Silver/Gold + MLflow smoke (Workflows job をトリガ)
	uv run python -u -m scripts.databricks.submit_job        # job_id を REST で run-now
databricks-parity: ## BQ ↔ Databricks の count/schema/metric parity
	uv run python -u -m scripts.data_platform.parity_check --target=databricks
```

`scripts/databricks/submit_job.py` は Databricks Jobs API `jobs/run-now` を叩いて完了まで poll（`scripts/ops/vertex/pipeline_wait.py` と同じパターン）。

### Phase 3 の完了確認
- `make databricks-parity` が exit 0、レポートに全観点 PASS
- 意図的に Databricks 側の 1 テーブルを 1 行削って parity が FAIL になることを確認（guard が効くこと）

---

## Phase 4 — Make target 整備 + docs 昇格（10I）

1. Makefile に追加（`run-all-core` には**入れない**）:
   ```
   data-platform-export / databricks-smoke / databricks-parity / snowflake-smoke / snowflake-parity
   ```
   `make help` のセクションは `# ----- Data Platform Add-ons (optional) -----` で分ける。`docs/conventions/Makefile規約.md` を再生成。
2. `docs/idea/data_platform_addons.md` を `docs/architecture/04_data_platform_addons.md` に昇格（or `docs/architecture/` に新規）。本手順書 (`docs/idea/data_platform_addons_runbook.md`) は `docs/runbook/06_data_platform_addons.md` に昇格 or そのまま `docs/idea/` に残す。
3. `docs/tasks/TASKS_ROADMAP.md` §1 の active backlog に「M-Wave10 Data Platform Add-ons」を追加（or §5 残マイルストーン）。`docs/architecture/03_実装カタログ.md` §2 実装クイックマップ / §3 Runtime に Data Platform 行を追加（完了後）。
4. contract test（軽量）: `tests/integration/parity/` に「`EXPORT_TABLES` のキーが idea doc の §7 高優先 3 テーブルと一致」「Makefile に `data-platform-export` / `databricks-parity` target が存在」「`run-all-core`（= `scripts/ops/run_all.py::STEPS`）に Databricks/Snowflake が**入っていない**ことを assert」（設計 §16-7 の破綻条件 guard）。
5. `make check` 全 PASS、`make check-layers: OK` を確認。

---

## Phase 5 — Snowflake トラック（並行 / 後回し可、10E/10F/10H）

Snowflake アカウントを取得してから。GCS Parquet（Phase 1 の出力）をそのまま使う。

1. `snowflake/sql/01_create_stage.sql`: GCP の Storage Integration（Snowflake → GCS）+ External Stage `@hybrid_search_stage` を `gs://mlops-dev-a-artifacts/data-platform-export/` に。
2. `02_create_raw_tables.sql`: `raw.user_actions` / `raw.ranking_labels` / `raw.property_features_daily`（Parquet schema に合わせた DDL、`VARIANT` で受けて後で展開でも可）。
3. `03_copy_into.sql`: `COPY INTO raw.user_actions FROM @hybrid_search_stage/user_actions/<date>/ FILE_FORMAT = (TYPE = PARQUET)`。
4. `04_create_marts.sql`: `mart.label_distribution` / `mart.feature_summary` 等の分析 mart。
5. `make snowflake-smoke`（`scripts/snowflake/` から SnowSQL or `snowflake-connector-python` で `.sql` を順次実行）/ `make snowflake-parity`（`parity_check.py --target=snowflake`、Databricks と同じ観点を Snowflake クエリで）。

設計 §9.4 の「やらないこと」（BigQuery 完全置換 / Snowpark ML 本格導入 / 本番 serving 経路に入れる / 全 feature_mart を移す）を守る。

---

## 完了条件（設計 §18 のチェックリスト）

- [ ] BigQuery から対象 3 テーブルを GCS Parquet に export できる（`make data-platform-export`）
- [ ] export manifest に 対象テーブル / 期間 / 件数 / GCS path / schema が記録される
- [ ] Databricks が Parquet を読み込み Bronze / Silver / Gold の最小処理を実行できる（`make databricks-smoke`）
- [ ] Databricks MLflow に LightGBM LambdaRank の training smoke run が記録される
- [ ] BigQuery ↔ Databricks の row count / schema / metric parity を確認できる（`make databricks-parity` exit 0）
- [ ] （Snowflake 着手時）Snowflake が External Stage 経由で Parquet を取り込み raw / mart を作れる + parity 確認できる
- [ ] 既存 `run-all-core` は変更しない（contract test で pin）
- [ ] docs 上で BigQuery / Databricks / Snowflake の責務分担が説明されている（`04_data_platform_addons.md`）

---

## 罠 / 注意点

| 罠 | 対策 |
|---|---|
| **BQ canonical tables が空のまま export** | `destroy-all` 後は BQ も消える。export 前に `make deploy-all` → `seed-test` → `run-all-core` 完走を確認、または最低 `make seed-test` だけでも実行（`property_features_daily` 等が埋まる）。manifest の row_count が 0 なら即 fail させる |
| **GCS export bucket が `destroy-all` で消える** | export は ephemeral 前提。Databricks/Snowflake の external table は再 export 後に再ロードが要る。長期保持したいなら export bucket だけ `prevent_destroy` の専用 module に分離（VVS Index/Endpoint と同じ pattern） |
| **Databricks Free Edition の compute / region 制約** | serverless のみ・compute 時間に上限。GCS からの read は cross-cloud egress（学習データは数 KB なので無視できる）。詰まったら §2.1 の「UC Volume に手動 cp」代替 |
| **GCS SA key を Databricks に登録する security** | 学習用は read-only SA + 短命 key（90日以内ローテーション）。本番は GCP↔Databricks の Workload Identity Federation。key は git に絶対入れない |
| **PAT の漏洩 / 期限** | `DATABRICKS_TOKEN` 環境変数で渡す。`~/.databrickscfg` は gitignore 配下。期限切れたら parity が 401 で落ちる → PAT 再発行 |
| **schema 型の名前差分で parity が誤検知** | BQ ↔ Databricks ↔ Snowflake の型マッピング表（`STRING↔string↔VARCHAR`, `INT64↔bigint↔NUMBER`, `FLOAT64↔double↔FLOAT`, `TIMESTAMP↔timestamp↔TIMESTAMP_NTZ`, `DATE↔date↔DATE`, `BOOL↔boolean↔BOOLEAN`, `REPEATED↔array↔ARRAY`）を `parity_check.py` 内に持って正規化してから比較 |
| **`run-all-core` に混ぜて本線を不安定化**（設計 §16-7） | 絶対に `scripts/ops/run_all.py::STEPS` に入れない。contract test で「Databricks/Snowflake target が STEPS に無い」を assert |
| **Databricks と Snowflake を「同じもの」として説明**（設計 §16-3） | Databricks = Lakehouse / Feature Engineering / MLflow、Snowflake = Enterprise DWH / Governance / BI mart。責務表（設計 §4.2 / §4.3）を docs に明記 |

---

## 最短クイックスタート（Databricks トラックだけ、~半日）

```bash
# 1. BQ canonical tables を埋める（destroy 済なら deploy から）
make deploy-all && make seed-test && make run-all-core      # or 既に稼働中なら make seed-test だけ

# 2. Phase 0/1 のコードを書く（scripts/data_platform/ 3 ファイル + Makefile target）
#    → make data-platform-export で GCS に Parquet + manifest が出る
make data-platform-export
gsutil ls -r gs://mlops-dev-a-artifacts/data-platform-export/

# 3. Databricks 側: Storage Credential + External Location を GCS export prefix に張る（UI）
#    → SQL editor で  LIST 'gs://mlops-dev-a-artifacts/data-platform-export/'  が叩ければ OK

# 4. databricks/notebooks/01..04 を書いて Workflows job 化 → run-now
make databricks-smoke

# 5. parity
make databricks-parity        # exit 0 = BQ ↔ Databricks 一致

# 6. （余裕があれば）docs 昇格 + contract test + Snowflake トラック
```

これで設計 §15 の「既存 BigQuery 基盤の行動ログ・正解データ・特徴量を GCS Parquet 経由で Databricks に取り込み、Bronze / Silver / Gold と MLflow 実験に接続できる」が実物で示せる。
