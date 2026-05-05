from __future__ import annotations

from datetime import datetime

import psycopg

from app.domain.labeling import RankingLabel
from app.services.protocols.label_repository import LabelRepository
from ml.common import get_logger


class PostgresLabelRepository(LabelRepository):
    def __init__(self, *, dsn: str) -> None:
        self._dsn = dsn
        self._logger = get_logger("app.adapters.postgres_label_repository")

    def write_ranking_labels(self, labels: list[RankingLabel]) -> None:
        if not labels:
            return
        sql = """
            INSERT INTO ranking_labels (search_id, property_id, relevance_label, label_source)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (search_id, property_id) DO UPDATE SET
                relevance_label = EXCLUDED.relevance_label,
                label_source = EXCLUDED.label_source,
                created_at = NOW()
        """
        rows = [
            (label.search_id, label.property_id, label.relevance_label, label.label_source)
            for label in labels
        ]
        try:
            with psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
                cur.executemany(sql, rows)
                conn.commit()
        except Exception:
            self._logger.exception("write_ranking_labels failed")

    def read_ranking_labels(self, *, since: datetime | None = None) -> list[RankingLabel]:
        sql = """
            SELECT search_id, property_id, relevance_label, label_source, created_at
            FROM ranking_labels
        """
        try:
            with psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
                params: tuple[datetime, ...] = ()
                if since is not None:
                    sql += "\nWHERE created_at >= %s"
                    params = (since,)
                sql += "\nORDER BY created_at ASC"
                cur.execute(sql, params)
                rows = cur.fetchall()
        except Exception:
            self._logger.exception("read_ranking_labels failed")
            return []
        return [
            RankingLabel(
                search_id=str(row[0]),
                property_id=str(row[1]),
                relevance_label=float(row[2]),
                label_source=str(row[3]),
                created_at=row[4],
            )
            for row in rows
        ]
