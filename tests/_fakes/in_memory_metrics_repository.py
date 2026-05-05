"""In-memory fake for :class:`MetricsRepository` (unit tests)."""

from __future__ import annotations

from datetime import datetime

from app.domain.training import EvaluationMetric
from app.services.protocols.metrics_repository import MetricsRepository


class InMemoryMetricsRepository(MetricsRepository):
    def __init__(self, metrics: list[EvaluationMetric] | None = None) -> None:
        self._metrics: list[EvaluationMetric] = list(metrics or [])

    def write_evaluation_metrics(self, metrics: list[EvaluationMetric]) -> None:
        self._metrics.extend(metrics)

    def read_evaluation_metrics(
        self,
        *,
        run_id: str | None = None,
        metric_name: str | None = None,
        since: datetime | None = None,
    ) -> list[EvaluationMetric]:
        records = list(self._metrics)
        if run_id is not None:
            records = [m for m in records if m.run_id == run_id]
        if metric_name is not None:
            records = [m for m in records if m.metric_name == metric_name]
        if since is not None:
            records = [m for m in records if m.evaluated_at >= since]
        records.sort(key=lambda m: m.evaluated_at, reverse=True)
        return records

    def latest_metrics(self, *, metric_names: list[str]) -> dict[str, EvaluationMetric]:
        out: dict[str, EvaluationMetric] = {}
        for metric in self._metrics:
            if metric.metric_name not in metric_names:
                continue
            current = out.get(metric.metric_name)
            if current is None or metric.evaluated_at > current.evaluated_at:
                out[metric.metric_name] = metric
        return out

    @property
    def metrics(self) -> list[EvaluationMetric]:
        """Test-only accessor."""
        return list(self._metrics)
