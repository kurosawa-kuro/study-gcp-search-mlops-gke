"""GCS-backed adapter for :class:`TrainingDatasetRepository`.

The training frame Parquet itself lives at ``<gcs_prefix>/<run_id>.parquet``;
this adapter only manages the **manifest JSON** at
``<gcs_prefix>/manifest.jsonl`` so the ``/ops/admin/mlops`` endpoint and
the Composer DAG ``monitoring_validation`` can list past runs without
re-scanning every Parquet object.

Each manifest line is a JSON record with ``uri`` / ``rows`` / ``created_at``
/ ``dataset_version`` / ``schema``. Append-only — never rewrites history.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

from google.cloud import storage

from app.domain.training import TrainingDatasetRef
from app.services.protocols.training_dataset_repository import TrainingDatasetRepository
from ml.common.logging import get_logger

_MANIFEST_OBJECT = "manifest.jsonl"


class GcsTrainingDatasetRepository(TrainingDatasetRepository):
    def __init__(
        self,
        *,
        client: storage.Client,
        bucket: str,
        prefix: str = "training_dataset",
    ) -> None:
        self._client = client
        self._bucket = bucket
        self._prefix = prefix.strip("/")
        self._logger = get_logger("app.adapters.gcs_training_dataset_repository")

    @property
    def _manifest_path(self) -> str:
        return f"{self._prefix}/{_MANIFEST_OBJECT}"

    def write_training_dataset(self, ref: TrainingDatasetRef) -> None:
        record = {
            "uri": ref.uri,
            "rows": int(ref.rows),
            "created_at": (ref.created_at or datetime.now(timezone.utc)).isoformat(),
            "dataset_version": ref.dataset_version,
            "schema": list(ref.schema),
        }
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
        try:
            bucket = self._client.bucket(self._bucket)
            blob = bucket.blob(self._manifest_path)
            existing = blob.download_as_text() if blob.exists(self._client) else ""
            blob.upload_from_string(existing + line, content_type="application/x-ndjson")
        except Exception:
            self._logger.exception(
                "write_training_dataset failed for uri=%s",
                ref.uri,
            )

    def read_training_dataset(self, *, since: datetime | None = None) -> list[TrainingDatasetRef]:
        records = self._read_manifest()
        if since is not None:
            records = [r for r in records if r.created_at and r.created_at >= since]
        records.sort(key=lambda r: r.created_at or datetime.min, reverse=True)
        return records

    def latest_training_dataset(self) -> TrainingDatasetRef | None:
        records = self.read_training_dataset()
        return records[0] if records else None

    def _read_manifest(self) -> list[TrainingDatasetRef]:
        try:
            bucket = self._client.bucket(self._bucket)
            blob = bucket.blob(self._manifest_path)
            if not blob.exists(self._client):
                return []
            text = blob.download_as_text()
        except Exception:
            self._logger.exception("read_training_dataset manifest read failed")
            return []
        out: list[TrainingDatasetRef] = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                self._logger.warning("skipping malformed manifest line")
                continue
            created_at_raw = record.get("created_at")
            try:
                created_at = (
                    datetime.fromisoformat(created_at_raw)
                    if isinstance(created_at_raw, str)
                    else None
                )
            except ValueError:
                created_at = None
            out.append(
                TrainingDatasetRef(
                    uri=str(record.get("uri", "")),
                    rows=int(record.get("rows", 0) or 0),
                    created_at=created_at,
                    dataset_version=(
                        str(record["dataset_version"])
                        if record.get("dataset_version") is not None
                        else None
                    ),
                    schema=list(record.get("schema") or []),
                )
            )
        return out
