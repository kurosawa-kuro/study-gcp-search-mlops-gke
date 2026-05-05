from __future__ import annotations

from datetime import datetime, timezone
from typing import cast

from google.cloud import bigquery

from app.domain.labeling import RankingLabel
from app.services.protocols.label_repository import LabelRepository
from ml.common.logging import get_logger


class BigQueryLabelRepository(LabelRepository):
    def __init__(
        self,
        *,
        client: bigquery.Client,
        ranking_labels_table: str,
    ) -> None:
        self._client = client
        self._ranking_labels_table = ranking_labels_table
        self._logger = get_logger("app.adapters.bigquery_label_repository")

    def write_ranking_labels(self, labels: list[RankingLabel]) -> None:
        if not labels:
            return
        merge_sql = f"""
            MERGE `{self._ranking_labels_table}` AS target
            USING (
              SELECT
                @search_id AS search_id,
                @property_id AS property_id,
                @relevance_label AS relevance_label,
                @label_source AS label_source,
                @created_at AS created_at
            ) AS source
            ON target.search_id = source.search_id
             AND target.property_id = source.property_id
            WHEN MATCHED THEN
              UPDATE SET
                relevance_label = source.relevance_label,
                label_source = source.label_source,
                created_at = source.created_at
            WHEN NOT MATCHED THEN
              INSERT (search_id, property_id, relevance_label, label_source, created_at)
              VALUES (
                source.search_id,
                source.property_id,
                source.relevance_label,
                source.label_source,
                source.created_at
              )
        """
        for label in labels:
            created_at = label.created_at or datetime.now(timezone.utc)
            try:
                self._client.query(
                    merge_sql,
                    job_config=bigquery.QueryJobConfig(
                        query_parameters=[
                            bigquery.ScalarQueryParameter("search_id", "STRING", label.search_id),
                            bigquery.ScalarQueryParameter(
                                "property_id", "STRING", label.property_id
                            ),
                            bigquery.ScalarQueryParameter(
                                "relevance_label", "INT64", int(label.relevance_label)
                            ),
                            bigquery.ScalarQueryParameter(
                                "label_source", "STRING", label.label_source
                            ),
                            bigquery.ScalarQueryParameter("created_at", "TIMESTAMP", created_at),
                        ]
                    ),
                ).result()
            except Exception:
                self._logger.exception(
                    "write_ranking_labels failed for search_id=%s property_id=%s",
                    label.search_id,
                    label.property_id,
                )

    def read_ranking_labels(self, *, since: datetime | None = None) -> list[RankingLabel]:
        sql = f"""
            SELECT
              search_id,
              property_id,
              relevance_label,
              label_source,
              created_at
            FROM `{self._ranking_labels_table}`
            {"WHERE created_at >= @since" if since is not None else ""}
            ORDER BY created_at ASC
        """
        params: list[bigquery.ScalarQueryParameter] = []
        if since is not None:
            params.append(bigquery.ScalarQueryParameter("since", "TIMESTAMP", since))
        try:
            rows = self._client.query(
                sql,
                job_config=bigquery.QueryJobConfig(query_parameters=params),
            ).result()
        except Exception:
            self._logger.exception("read_ranking_labels failed")
            return []
        return [
            RankingLabel(
                search_id=str(row["search_id"]),
                property_id=str(row["property_id"]),
                relevance_label=int(cast(int | str, row["relevance_label"])),
                label_source=str(row["label_source"]),
                created_at=cast(datetime | None, row["created_at"]),
            )
            for row in rows
        ]
