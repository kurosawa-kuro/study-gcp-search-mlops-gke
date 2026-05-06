"""Lexical retrieval via Elasticsearch BM25 (canonical Phase 7+ lexical lane)."""

from __future__ import annotations

from typing import Any

import httpx

from app.domain.retrieval import LexicalResult
from app.domain.search import SearchFilters
from app.services.protocols.lexical_search import LexicalSearchPort
from ml.common import get_logger


class ElasticsearchLexical(LexicalSearchPort):
    """BM25 search against an Elasticsearch index (documents from ``sync_elasticsearch``)."""

    def __init__(
        self,
        *,
        base_url: str,
        index_name: str = "properties",
        timeout_seconds: float = 3.0,
        api_key: str = "",
        username: str = "",
        password: str = "",
        verify_tls: bool = True,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._index_name = index_name
        self._timeout_seconds = timeout_seconds
        self._api_key = api_key.strip()
        self._username = username.strip()
        self._password = password
        self._verify_tls = verify_tls
        self._logger = get_logger("app.adapters.elasticsearch_lexical")

    def _headers(self) -> dict[str, str]:
        h = {"content-type": "application/json"}
        if self._api_key:
            h["authorization"] = f"ApiKey {self._api_key}"
        return h

    def search(
        self,
        *,
        query: str,
        filters: SearchFilters,
        top_k: int,
    ) -> list[LexicalResult]:
        filter_clauses = _filters_to_es(filters)
        body: dict[str, Any] = {
            "size": top_k,
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^2", "city", "ward", "layout"],
                                "type": "best_fields",
                            }
                        }
                    ],
                }
            },
            "_source": ["property_id"],
        }
        if filter_clauses:
            body["query"]["bool"]["filter"] = filter_clauses

        url = f"{self._base_url}/{self._index_name}/_search"
        try:
            auth = None
            if self._username and self._password:
                auth = (self._username, self._password)
            with httpx.Client(
                timeout=self._timeout_seconds,
                auth=auth,
                verify=self._verify_tls,
            ) as client:
                resp = client.post(url, json=body, headers=self._headers())
                resp.raise_for_status()
                data = resp.json()
        except Exception:
            self._logger.exception("Elasticsearch lexical request failed")
            return []

        hits = (data.get("hits") or {}).get("hits") or []
        out: list[LexicalResult] = []
        for idx, hit in enumerate(hits, start=1):
            src = hit.get("_source") if isinstance(hit.get("_source"), dict) else {}
            pid = str(hit.get("_id") or src.get("property_id") or "").strip()
            if not pid:
                continue
            out.append(LexicalResult(property_id=pid, rank=idx))
        return out


def _filters_to_es(filters: SearchFilters) -> list[dict[str, Any]]:
    clauses: list[dict[str, Any]] = []
    max_rent = filters.get("max_rent")
    if max_rent is not None:
        clauses.append({"range": {"rent": {"lte": int(max_rent)}}})

    layout = filters.get("layout")
    if layout:
        clauses.append({"term": {"layout": str(layout)}})

    max_walk_min = filters.get("max_walk_min")
    if max_walk_min is not None:
        clauses.append({"range": {"walk_min": {"lte": int(max_walk_min)}}})

    pet_ok = filters.get("pet_ok")
    if pet_ok is not None:
        clauses.append({"term": {"pet_ok": bool(pet_ok)}})

    max_age = filters.get("max_age")
    if max_age is not None:
        clauses.append({"range": {"age_years": {"lte": int(max_age)}}})

    return clauses
