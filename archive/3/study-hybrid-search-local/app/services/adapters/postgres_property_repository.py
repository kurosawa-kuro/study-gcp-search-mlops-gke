from __future__ import annotations

import psycopg

from app.domain.property import Property
from app.services.protocols.property_repository import PropertyRepository
from ml.common import get_logger


class PostgresPropertyRepository(PropertyRepository):
    def __init__(self, *, dsn: str) -> None:
        self._dsn = dsn
        self._logger = get_logger("app.adapters.postgres_property_repository")

    def fetch(self, property_id: str) -> Property | None:
        sql = """
            SELECT property_id, title, description, city, ward, layout, rent,
                   walk_min, age_years, area_m2, pet_ok, created_at
            FROM properties
            WHERE property_id = %s
            LIMIT 1
        """
        try:
            with psycopg.connect(self._dsn) as conn, conn.cursor() as cur:
                cur.execute(sql, (property_id,))
                row = cur.fetchone()
        except Exception:
            self._logger.exception("fetch property failed")
            return None
        if row is None:
            return None
        return Property(
            property_id=str(row[0]),
            title=str(row[1]),
            description=str(row[2]),
            city=str(row[3]),
            ward=None if row[4] is None else str(row[4]),
            layout=str(row[5]),
            rent=int(row[6]),
            walk_min=int(row[7]),
            age_years=int(row[8]),
            area_m2=float(row[9]),
            pet_ok=bool(row[10]),
            created_at=row[11],
        )
