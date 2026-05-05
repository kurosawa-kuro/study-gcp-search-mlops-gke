"""Domain types for training-dataset / evaluation-metric handoff."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TrainingDatasetRef:
    """Pointer to a serialized training frame in object storage.

    The training frame itself (Parquet rows) is too large for a Python
    dataclass; the Composer DAG / Vertex AI Pipelines hand off only the
    URI + counts here so downstream consumers know where to read from.
    """

    uri: str
    rows: int
    created_at: datetime | None = None
    dataset_version: str | None = None
    schema: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvaluationMetric:
    """A single row of the BigQuery ``mlops.evaluation_metrics`` table.

    Maps 1:1 to the Terraform schema in
    ``infra/terraform/modules/data/main.tf`` (canonical metric_name set:
    ``ndcg_at_10`` / ``recall_at_20`` / ``map`` / ``ctr`` / ``cvr``).
    ``passed`` carries the deployment-gate verdict; ``None`` = not yet
    evaluated against a threshold.
    """

    run_id: str
    metric_name: str
    metric_value: float
    evaluated_at: datetime
    threshold: float | None = None
    passed: bool | None = None
    dataset_version: str | None = None
