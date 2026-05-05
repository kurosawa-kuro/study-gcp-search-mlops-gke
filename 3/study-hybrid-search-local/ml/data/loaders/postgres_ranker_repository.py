from __future__ import annotations

from datetime import datetime

import pandas as pd
import psycopg

from ml.data.feature_engineering import FEATURE_COLS_RANKER, RANKER_GROUP_COL, RANKER_LABEL_COL


class PostgresRankerRepository:
    def __init__(self, *, dsn: str) -> None:
        self._dsn = dsn

    def read_training_data(self, *, since: datetime | None = None) -> pd.DataFrame:
        sql = """
            SELECT
                rl.search_id AS request_id,
                rl.property_id,
                GREATEST(rl.relevance_label, 0) AS label,
                p.rent,
                p.walk_min,
                p.age_years,
                p.area_m2,
                fm.ctr,
                fm.fav_rate,
                fm.inquiry_rate,
                si.vector_score AS me5_score,
                COALESCE(si.lexical_rank_orig, 0) AS lexical_rank,
                COALESCE(si.semantic_rank_orig, 0) AS semantic_rank
            FROM ranking_labels AS rl
            JOIN search_impressions AS si
              ON si.search_id = rl.search_id
             AND si.property_id = rl.property_id
            JOIN properties AS p
              ON p.property_id = rl.property_id
            LEFT JOIN feature_mart_property_features_daily AS fm
              ON fm.property_id = rl.property_id
        """
        params: tuple[datetime, ...] = ()
        if since is not None:
            sql += "\nWHERE rl.created_at >= %s"
            params = (since,)
        sql += "\nORDER BY rl.search_id ASC, si.rank ASC"

        with psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            columns = [desc.name for desc in cur.description or ()]
        df = pd.DataFrame(rows, columns=columns)
        if df.empty:
            return df
        df["label"] = df["label"].astype(int)
        numeric_cols = FEATURE_COLS_RANKER + [RANKER_LABEL_COL]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
        df[RANKER_LABEL_COL] = df[RANKER_LABEL_COL].astype(int)
        ordered = [RANKER_GROUP_COL, "property_id", RANKER_LABEL_COL, *FEATURE_COLS_RANKER]
        return df[ordered]
