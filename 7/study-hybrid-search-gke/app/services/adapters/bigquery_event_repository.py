from __future__ import annotations

import json
from datetime import datetime
from typing import cast

from google.cloud import bigquery

from app.domain.event import ActionType, Impression, SearchEvent, UserAction
from app.services.protocols.event_repository import EventRepository
from ml.common.logging import get_logger


class BigQueryEventRepository(EventRepository):
    def __init__(
        self,
        *,
        client: bigquery.Client,
        search_events_table: str,
        search_impressions_table: str,
        user_actions_table: str,
    ) -> None:
        self._client = client
        self._search_events_table = search_events_table
        self._search_impressions_table = search_impressions_table
        self._user_actions_table = user_actions_table
        self._logger = get_logger("app.adapters.bigquery_event_repository")

    def read_search_events(self, *, since: datetime | None = None) -> list[SearchEvent]:
        sql = f"""
            SELECT
              search_id,
              query,
              filters_json,
              user_id,
              session_id,
              app_version,
              model_version,
              timestamp
            FROM `{self._search_events_table}`
            {_where_clause([("timestamp >= @since", since is not None)])}
            ORDER BY timestamp ASC
        """
        rows = self._query(sql, _scalar_params(since=since))
        return [
            SearchEvent(
                search_id=str(row["search_id"]),
                query=str(row["query"]),
                filters_json=_json_text(row.get("filters_json")),
                user_id=_optional_str(row.get("user_id")),
                session_id=_optional_str(row.get("session_id")),
                app_version=_optional_str(row.get("app_version")),
                model_version=_optional_str(row.get("model_version")),
                timestamp=cast(datetime | None, row.get("timestamp")),
            )
            for row in rows
        ]

    def read_impressions(
        self,
        *,
        search_id: str | None = None,
        since: datetime | None = None,
    ) -> list[Impression]:
        sql = f"""
            SELECT
              search_id,
              property_id,
              rank,
              lexical_rank_orig,
              semantic_rank_orig,
              lexical_score,
              vector_score,
              rrf_score,
              rerank_score,
              timestamp
            FROM `{self._search_impressions_table}`
            {_where_clause([
                ("search_id = @search_id", search_id is not None),
                ("timestamp >= @since", since is not None),
            ])}
            ORDER BY timestamp ASC, rank ASC
        """
        rows = self._query(sql, _scalar_params(search_id=search_id, since=since))
        return [
            Impression(
                search_id=str(row["search_id"]),
                property_id=str(row["property_id"]),
                rank=int(cast(int | str, row["rank"])),
                lexical_rank_orig=_optional_int(row.get("lexical_rank_orig")),
                semantic_rank_orig=_optional_int(row.get("semantic_rank_orig")),
                lexical_score=_optional_float(row.get("lexical_score")),
                vector_score=_optional_float(row.get("vector_score")),
                rrf_score=_optional_float(row.get("rrf_score")),
                rerank_score=_optional_float(row.get("rerank_score")),
                timestamp=cast(datetime | None, row.get("timestamp")),
            )
            for row in rows
        ]

    def read_user_actions(
        self,
        *,
        search_id: str | None = None,
        action_type: str | None = None,
        since: datetime | None = None,
    ) -> list[UserAction]:
        sql = f"""
            SELECT
              search_id,
              property_id,
              action_type,
              action_value,
              timestamp
            FROM `{self._user_actions_table}`
            {_where_clause([
                ("search_id = @search_id", search_id is not None),
                ("action_type = @action_type", action_type is not None),
                ("timestamp >= @since", since is not None),
            ])}
            ORDER BY timestamp ASC
        """
        rows = self._query(
            sql,
            _scalar_params(search_id=search_id, action_type=action_type, since=since),
        )
        return [
            UserAction(
                search_id=str(row["search_id"]),
                property_id=str(row["property_id"]),
                action_type=cast(ActionType, str(row["action_type"])),
                action_value=_optional_float(row.get("action_value")),
                timestamp=cast(datetime | None, row.get("timestamp")),
            )
            for row in rows
        ]

    def _query(
        self,
        sql: str,
        params: list[bigquery.ScalarQueryParameter],
    ) -> list[dict[str, object | None]]:
        try:
            job = self._client.query(
                sql,
                job_config=bigquery.QueryJobConfig(query_parameters=params),
            )
            return [dict(row.items()) for row in job.result()]
        except Exception:
            self._logger.exception("event repository query failed")
            return []


def _where_clause(conditions: list[tuple[str, bool]]) -> str:
    active = [fragment for fragment, enabled in conditions if enabled]
    if not active:
        return ""
    return "WHERE " + " AND ".join(active)


def _scalar_params(
    *,
    search_id: str | None = None,
    action_type: str | None = None,
    since: datetime | None = None,
) -> list[bigquery.ScalarQueryParameter]:
    params: list[bigquery.ScalarQueryParameter] = []
    if search_id is not None:
        params.append(bigquery.ScalarQueryParameter("search_id", "STRING", search_id))
    if action_type is not None:
        params.append(bigquery.ScalarQueryParameter("action_type", "STRING", action_type))
    if since is not None:
        params.append(bigquery.ScalarQueryParameter("since", "TIMESTAMP", since))
    return params


def _optional_str(value: object | None) -> str | None:
    return None if value is None else str(value)


def _optional_int(value: object | None) -> int | None:
    return None if value is None else int(cast(int | str, value))


def _optional_float(value: object | None) -> float | None:
    return None if value is None else float(cast(float | int | str, value))


def _json_text(value: object | None) -> str:
    if value is None:
        return "{}"
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
