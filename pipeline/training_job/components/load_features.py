"""KFP component: fetch the LambdaRank training frame from BigQuery.

Wave 4 死守ライン (canonical 死守):
    本 component は **BigQuery を実際にクエリする**。`ranking_labels` x
    `search_impressions` x latest `feature_mart.property_features_daily` を
    join した training frame を Parquet に書き出し、下流の `train_reranker`
    に渡す。stub だった旧版 (JSON metadata のみ書き出し) を撤去。

経路: ``mlops.ranking_labels`` を含む 6 canonical 場所 (Pydantic /
Terraform / labeling YAML / labeling SQL / EventWriter Port / ranking_labels
書き込み) で `action_type` enum と weight が一致している前提で、本 component
が SELECT した relevance_label がそのまま LightGBM LambdaRank の label に流れる。
"""

from kfp import dsl


@dsl.component(
    base_image="python:3.12",
    packages_to_install=[
        "google-cloud-bigquery>=3.27,<4.0",
        "google-cloud-bigquery-storage>=2.27,<3.0",
        "pandas>=2.2,<3.0",
        "pyarrow>=18.0,<22.0",
        "db-dtypes>=1.3,<2.0",
    ],
)
def load_features(
    project_id: str,
    feature_dataset_id: str,
    feature_table: str,
    mlops_dataset_id: str,
    ranking_log_table: str,
    search_impressions_table: str,
    ranking_labels_table: str,
    window_days: int,
    training_frame: dsl.Output[dsl.Dataset],
) -> None:
    import sys
    import traceback

    def _log(msg: str) -> None:
        print(f"[load_features] {msg}", flush=True)
        print(f"[load_features] {msg}", file=sys.stderr, flush=True)

    _log("STEP 1 — component entry")
    _log(f"  project_id={project_id}")
    _log(f"  feature_dataset_id={feature_dataset_id} feature_table={feature_table}")
    _log(f"  mlops_dataset_id={mlops_dataset_id} ranking_log_table={ranking_log_table}")
    _log(
        "  search_impressions_table="
        f"{search_impressions_table} ranking_labels_table={ranking_labels_table} "
        f"window_days={window_days}"
    )
    _log(f"  training_frame.uri={training_frame.uri} path={training_frame.path}")

    try:
        from pathlib import Path

        import pandas as pd
        from google.cloud import bigquery

        query = f"""
        WITH latest_features AS (
          SELECT
            property_id,
            rent,
            walk_min,
            age_years,
            area_m2,
            ctr,
            fav_rate,
            inquiry_rate
          FROM `{project_id}.{feature_dataset_id}.{feature_table}`
          WHERE event_date = (
            SELECT MAX(event_date)
            FROM `{project_id}.{feature_dataset_id}.{feature_table}`
          )
        )
        SELECT
          rl.search_id AS request_id,
          rl.property_id,
          COALESCE(f.rent, r.features.rent) AS rent,
          COALESCE(f.walk_min, r.features.walk_min) AS walk_min,
          COALESCE(f.age_years, r.features.age_years) AS age_years,
          COALESCE(f.area_m2, r.features.area_m2) AS area_m2,
          COALESCE(f.ctr, r.features.ctr) AS ctr,
          COALESCE(f.fav_rate, r.features.fav_rate) AS fav_rate,
          COALESCE(f.inquiry_rate, r.features.inquiry_rate) AS inquiry_rate,
          COALESCE(si.vector_score, r.features.me5_score) AS me5_score,
          COALESCE(CAST(si.lexical_rank_orig AS FLOAT64), r.features.lexical_rank) AS lexical_rank,
          COALESCE(CAST(si.semantic_rank_orig AS FLOAT64), r.features.semantic_rank, 0.0) AS semantic_rank,
          GREATEST(rl.relevance_label, 0) AS label
        FROM `{project_id}.{mlops_dataset_id}.{ranking_labels_table}` rl
        JOIN `{project_id}.{mlops_dataset_id}.{search_impressions_table}` si
          ON si.search_id = rl.search_id
         AND si.property_id = rl.property_id
        LEFT JOIN `{project_id}.{mlops_dataset_id}.{ranking_log_table}` r
          ON r.request_id = rl.search_id
         AND r.property_id = rl.property_id
        LEFT JOIN latest_features f
          USING (property_id)
        WHERE rl.created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {window_days} DAY)
        ORDER BY rl.search_id, si.rank
        """.strip()

        _log("STEP 2 — BigQuery client init")
        client = bigquery.Client(project=project_id)

        _log("STEP 3 — execute query")
        df: pd.DataFrame = client.query(query).result().to_dataframe(create_bqstorage_client=True)
        _log(f"  fetched rows={len(df)} columns={list(df.columns)}")

        if df.empty:
            _log(
                "WARNING — empty training frame. Composer DAG will short-circuit "
                "the train_reranker stage; check ranking_labels coverage / window_days."
            )

        _log(f"STEP 4 — write Parquet to {training_frame.path}")
        out_path = Path(training_frame.path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out_path, index=False)
        _log(f"  wrote {out_path.stat().st_size} bytes")

        # Metadata for downstream visibility (KFP UI / lineage). The actual
        # training frame is the Parquet payload above — metadata は補足のみ。
        training_frame.metadata.update(
            {
                "rows": len(df),
                "columns": list(df.columns),
                "window_days": int(window_days),
                "split_strategy": "FARM_FINGERPRINT(request_id) % 10 < 8",
                "ranking_labels_table": (f"{project_id}.{mlops_dataset_id}.{ranking_labels_table}"),
            }
        )
        _log("DONE")
    except Exception:
        _log("ERROR in load_features")
        _log(traceback.format_exc())
        raise
