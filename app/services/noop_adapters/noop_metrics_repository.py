"""Noop fallback for :class:`MetricsRepository`."""

from __future__ import annotations

from datetime import datetime

from app.domain.training import EvaluationMetric
from app.services.protocols.metrics_repository import MetricsRepository


class NoopMetricsRepository(MetricsRepository):
    """Returns no-ops; used when BigQuery is not configured."""

    def write_evaluation_metrics(self, metrics: list[EvaluationMetric]) -> None:  # noqa: ARG002
        return None

    def read_evaluation_metrics(
        self,
        *,
        run_id: str | None = None,  # noqa: ARG002
        metric_name: str | None = None,  # noqa: ARG002
        since: datetime | None = None,  # noqa: ARG002
    ) -> list[EvaluationMetric]:
        return []

    def latest_metrics(
        self,
        *,
        metric_names: list[str],  # noqa: ARG002
    ) -> dict[str, EvaluationMetric]:
        return {}
