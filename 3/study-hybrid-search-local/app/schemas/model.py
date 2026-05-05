"""Pydantic schemas for /model/* endpoints in Phase 3."""

from __future__ import annotations

from pydantic import BaseModel


class CaseMetric(BaseModel):
    name: str
    query: str
    returned: int
    relevant_total: int
    matched_in_results: int
    ndcg_at_k: float
    hit_rate_at_k: float
    mrr_at_k: float


class AccuracySummary(BaseModel):
    ndcg_at_k: float
    hit_rate_at_k: float
    mrr_at_k: float


class ModelMetricsResponse(BaseModel):
    cases_file: str
    num_cases: int
    k: int
    summary: AccuracySummary
    per_case: list[CaseMetric]


class ModelInfoResponse(BaseModel):
    encoder_endpoint: str
    encoder_model_path: str | None = None
    reranker_endpoint: str
    reranker_model_path: str | None = None
    rerank_enabled: bool
    search_enabled: bool


class DataPreviewTable(BaseModel):
    key: str
    title: str
    description: str
    table_fqn: str
    latest_marker: str | None = None
    columns: list[str]
    rows: list[dict[str, object | None]]


class ModelDataResponse(BaseModel):
    tables: list[DataPreviewTable]
