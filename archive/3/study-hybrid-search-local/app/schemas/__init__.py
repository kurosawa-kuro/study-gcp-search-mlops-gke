"""Pydantic request / response schemas for the FastAPI endpoints."""

from .model import (
    AccuracySummary,
    CaseMetric,
    DataPreviewTable,
    ModelDataResponse,
    ModelInfoResponse,
    ModelMetricsResponse,
)
from .search import (
    FeedbackRequest,
    FeedbackResponse,
    SearchFilters,
    SearchRequest,
    SearchResponse,
    SearchResultItem,
)

__all__ = [
    "AccuracySummary",
    "CaseMetric",
    "DataPreviewTable",
    "FeedbackRequest",
    "FeedbackResponse",
    "ModelDataResponse",
    "ModelInfoResponse",
    "ModelMetricsResponse",
    "SearchFilters",
    "SearchRequest",
    "SearchResponse",
    "SearchResultItem",
]
