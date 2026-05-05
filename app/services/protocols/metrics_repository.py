"""Port: read / write evaluation metrics for the deployment gate.

Maps onto BigQuery ``mlops.evaluation_metrics`` (Terraform-managed). The
Composer DAG ``monitoring_validation`` writes per-metric rows; the
``/ops/admin/mlops`` endpoint and the same DAG's gate task read them.
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from app.domain.training import EvaluationMetric


class MetricsRepository(Protocol):
    def write_evaluation_metrics(self, metrics: list[EvaluationMetric]) -> None:
        """Append rows to ``mlops.evaluation_metrics``."""
        ...

    def read_evaluation_metrics(
        self,
        *,
        run_id: str | None = None,
        metric_name: str | None = None,
        since: datetime | None = None,
    ) -> list[EvaluationMetric]:
        """Return metrics filtered by run_id / metric_name / since (newest first)."""
        ...

    def latest_metrics(self, *, metric_names: list[str]) -> dict[str, EvaluationMetric]:
        """Most recent value of each requested metric (skipped if absent)."""
        ...
