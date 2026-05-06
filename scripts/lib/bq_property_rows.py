"""Shared BigQuery row load for lexical index sync (Elasticsearch bulk upsert)."""

from __future__ import annotations

from typing import Any

from google.cloud import bigquery


def load_properties_cleaned_rows(*, client: bigquery.Client, fq_table: str) -> list[dict[str, Any]]:
    """Load rows from ``feature_mart.properties_cleaned`` for lexical indexing."""
    query = f"""
        SELECT
          property_id,
          title,
          city,
          ward,
          layout,
          rent,
          walk_min,
          age_years,
          pet_ok
        FROM `{fq_table}`
    """
    rows = client.query(query).result()
    out: list[dict[str, Any]] = []
    for row in rows:
        out.append(
            {
                "property_id": row["property_id"],
                "title": row["title"],
                "city": row["city"],
                "ward": row["ward"],
                "layout": row["layout"],
                "rent": row["rent"],
                "walk_min": row["walk_min"],
                "age_years": row["age_years"],
                "pet_ok": row["pet_ok"],
            }
        )
    return out
