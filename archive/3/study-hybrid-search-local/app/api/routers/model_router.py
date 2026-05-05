"""Local Phase 3 /model/* endpoints."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Annotated, Any, cast

import psycopg
from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_container
from app.composition_root import Container
from app.schemas.model import (
    AccuracySummary,
    CaseMetric,
    DataPreviewTable,
    ModelDataResponse,
    ModelInfoResponse,
    ModelMetricsResponse,
)
from app.services.model_metrics_service import ModelMetricsService, default_cases_path

router = APIRouter(prefix="/model")


@router.get("/metrics", response_model=ModelMetricsResponse)
def model_metrics(
    container: Annotated[Container, Depends(get_container)],
    k: int = Query(default=10, ge=1, le=100),
) -> ModelMetricsResponse:
    service = ModelMetricsService(
        search_service=container.search_service,
        default_cases_file=default_cases_path(),
    )
    report = service.evaluate(k=k)
    return ModelMetricsResponse(
        cases_file=report.cases_file,
        num_cases=report.num_cases,
        k=report.k,
        summary=AccuracySummary(
            ndcg_at_k=report.summary_ndcg_at_k,
            hit_rate_at_k=report.summary_hit_rate_at_k,
            mrr_at_k=report.summary_mrr_at_k,
        ),
        per_case=[
            CaseMetric(
                name=c.name,
                query=c.query,
                returned=c.returned,
                relevant_total=c.relevant_total,
                matched_in_results=c.matched_in_results,
                ndcg_at_k=c.ndcg_at_k,
                hit_rate_at_k=c.hit_rate_at_k,
                mrr_at_k=c.mrr_at_k,
            )
            for c in report.per_case
        ],
    )


@router.get("/info", response_model=ModelInfoResponse)
def model_info(container: Annotated[Container, Depends(get_container)]) -> ModelInfoResponse:
    settings = container.settings
    return ModelInfoResponse(
        encoder_endpoint=f"in-process:{settings.e5_model_name}",
        encoder_model_path=settings.e5_model_name,
        reranker_endpoint="in-process:lightgbm",
        reranker_model_path=container.model_path,
        rerank_enabled=container.reranker_client is not None,
        search_enabled=settings.enable_search,
    )


@router.get("/data", response_model=ModelDataResponse)
def model_data(container: Annotated[Container, Depends(get_container)]) -> ModelDataResponse:
    settings = container.settings
    tables = [
        _query_preview(
            dsn=settings.postgres_dsn,
            key="feature-mart",
            title="Feature Mart",
            description="Phase 3 Local feature_mart_property_features_daily preview",
            table_fqn="postgres.feature_mart_property_features_daily",
            sql="""
                SELECT property_id, ctr, fav_rate, inquiry_rate, snapshot_date
                FROM feature_mart_property_features_daily
                ORDER BY snapshot_date DESC, property_id ASC
                LIMIT 10
            """,
        ),
        _query_preview(
            dsn=settings.postgres_dsn,
            key="ranking-labels",
            title="Ranking Labels",
            description="Wave 6 labeling output preview",
            table_fqn="postgres.ranking_labels",
            sql="""
                SELECT search_id, property_id, relevance_label, label_source, created_at
                FROM ranking_labels
                ORDER BY created_at DESC
                LIMIT 10
            """,
        ),
        _query_preview(
            dsn=settings.postgres_dsn,
            key="search-impressions",
            title="Search Impressions",
            description="Wave 5 search_impressions preview",
            table_fqn="postgres.search_impressions",
            sql="""
                SELECT search_id, property_id, rank, lexical_rank_orig, semantic_rank_orig, rerank_score, timestamp
                FROM search_impressions
                ORDER BY timestamp DESC
                LIMIT 10
            """,
        ),
        _csv_preview(
            artifacts_root=Path(settings.model_artifacts_root),
            key="training-dataset",
            title="Training Dataset",
            description="Latest generated training dataset CSV preview",
        ),
    ]
    return ModelDataResponse(tables=tables)


def _query_preview(
    *,
    dsn: str,
    key: str,
    title: str,
    description: str,
    table_fqn: str,
    sql: str,
) -> DataPreviewTable:
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(sql)
        rows_raw = cur.fetchall()
        columns = [desc[0] for desc in cast(list[Any], cur.description or [])]
    rows = [
        {str(col): _jsonable(value) for col, value in zip(columns, row, strict=True)}
        for row in rows_raw
    ]
    return DataPreviewTable(
        key=key,
        title=title,
        description=description,
        table_fqn=table_fqn,
        columns=[str(col) for col in columns],
        rows=rows,
        latest_marker=(str(rows[0].get(columns[-1])) if rows and columns else None),
    )


def _csv_preview(
    *,
    artifacts_root: Path,
    key: str,
    title: str,
    description: str,
) -> DataPreviewTable:
    latest = _latest_dataset_csv(artifacts_root)
    if latest is None:
        return DataPreviewTable(
            key=key,
            title=title,
            description=description,
            table_fqn="local.csv:not-found",
            columns=["message"],
            rows=[{"message": "training dataset not generated yet"}],
        )
    with latest.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [dict(row) for _, row in zip(range(10), reader, strict=False)]
        columns = list(reader.fieldnames or [])
    return DataPreviewTable(
        key=key,
        title=title,
        description=description,
        table_fqn=str(latest),
        latest_marker=str(latest.parent.name),
        columns=columns,
        rows=rows,
    )


def _latest_dataset_csv(artifacts_root: Path) -> Path | None:
    root = artifacts_root
    if not root.is_absolute():
        root = Path(__file__).resolve().parents[3] / root
    dataset_root = root / "datasets"
    if not dataset_root.exists():
        return None
    candidates = sorted(dataset_root.glob("*/training_dataset.csv"), reverse=True)
    return candidates[0] if candidates else None


def _jsonable(value: object) -> object | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        try:
            return str(value.isoformat())
        except Exception:
            return str(value)
    return value
