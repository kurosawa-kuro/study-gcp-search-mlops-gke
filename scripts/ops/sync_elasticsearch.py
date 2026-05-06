"""Elasticsearch index sync — BigQuery ``properties_cleaned`` → ES bulk upsert.

Upserts ``feature_mart.properties_cleaned`` rows into an Elasticsearch index
(default ``properties``). Used by ``make sync-elasticsearch`` and deploy-all
step ``sync-elasticsearch``.

Authentication (optional):
- ``ELASTICSEARCH_API_KEY`` — sent as ``Authorization: ApiKey <value>`` when set.
  Otherwise no auth header (dev single-node with ``xpack.security.enabled=false``).
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import socket
import subprocess
import sys
import time
import traceback
from typing import Any
from urllib.parse import urlparse, urlunparse

import httpx
from google.cloud import bigquery

from scripts.lib.bq_property_rows import load_properties_cleaned_rows


def _log(msg: str) -> None:
    print(f"[sync_elasticsearch] {msg}", flush=True)
    print(f"[sync_elasticsearch] {msg}", file=sys.stderr, flush=True)


def _headers(*, api_key: str) -> dict[str, str]:
    h = {"content-type": "application/json"}
    if api_key.strip():
        # Elastic Cloud style single header; also works for raw Base64(id:key).
        h["authorization"] = f"ApiKey {api_key.strip()}"
    return h


def _ensure_index(*, client: httpx.Client, base: str, index: str, headers: dict[str, str]) -> None:
    mapping = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "property_id": {"type": "keyword"},
                "title": {"type": "text"},
                "city": {"type": "text"},
                "ward": {"type": "text"},
                "layout": {"type": "keyword"},
                "rent": {"type": "integer"},
                "walk_min": {"type": "integer"},
                "age_years": {"type": "integer"},
                "pet_ok": {"type": "boolean"},
            }
        },
    }
    url = f"{base}/{index}"
    head = client.head(url, headers=headers)
    if head.status_code == 200:
        _log(f"index exists: {index}")
        return
    if head.status_code not in (404,):
        head.raise_for_status()
    _log(f"creating index {index}")
    resp = client.put(url, json=mapping, headers=headers)
    resp.raise_for_status()


def _bulk_upsert(
    *,
    client: httpx.Client,
    base: str,
    index: str,
    rows: list[dict[str, Any]],
    headers: dict[str, str],
    batch_size: int,
) -> None:
    bulk_url = f"{base}/_bulk"
    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        lines: list[str] = []
        for doc in batch:
            pid = str(doc.get("property_id") or "").strip()
            if not pid:
                continue
            lines.append(json.dumps({"index": {"_index": index, "_id": pid}}))
            lines.append(json.dumps(doc))
        if not lines:
            continue
        body = "\n".join(lines) + "\n"
        hdrs = dict(headers)
        hdrs["content-type"] = "application/x-ndjson"
        resp = client.post(bulk_url, content=body.encode("utf-8"), headers=hdrs)
        resp.raise_for_status()
        payload = resp.json()
        if payload.get("errors"):
            _log(f"bulk errors in batch [{i}:{i + len(batch)}]: {payload!s}"[:500])
            raise RuntimeError("Elasticsearch bulk reported errors=true")


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Sync properties_cleaned -> Elasticsearch")
    p.add_argument("--project-id", default=os.environ.get("PROJECT_ID", ""))
    p.add_argument(
        "--table",
        default=os.environ.get("BQ_PROPERTIES_TABLE", "feature_mart.properties_cleaned"),
    )
    p.add_argument("--es-url", default=os.environ.get("ELASTICSEARCH_URL", "").strip())
    p.add_argument("--index", default=os.environ.get("ELASTICSEARCH_INDEX", "properties"))
    p.add_argument("--api-key", default=os.environ.get("ELASTICSEARCH_API_KEY", ""))
    p.add_argument("--username", default=os.environ.get("ELASTICSEARCH_USERNAME", ""))
    p.add_argument("--password", default=os.environ.get("ELASTICSEARCH_PASSWORD", ""))
    p.add_argument("--batch-size", type=int, default=200)
    return p.parse_args(argv)


@contextlib.contextmanager
def _maybe_port_forward_for_cluster_dns(es_url: str):
    """Expose cluster-local Elasticsearch via localhost when run outside cluster."""
    parsed = urlparse(es_url)
    host = parsed.hostname or ""
    if not host.endswith(".svc.cluster.local"):
        yield es_url
        return

    local_port = 19200
    forwarded_url = urlunparse(
        (parsed.scheme or "http", f"127.0.0.1:{local_port}", parsed.path, "", "", "")
    )
    cmd = [
        "kubectl",
        "port-forward",
        "--namespace=search",
        "service/elasticsearch",
        f"{local_port}:9200",
    ]
    _log("cluster-local ES detected; starting kubectl port-forward to localhost:19200")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        ready = False
        for _ in range(20):
            if proc.poll() is not None:
                break
            try:
                with socket.create_connection(("127.0.0.1", local_port), timeout=1.0):
                    ready = True
                    break
            except OSError:
                time.sleep(0.5)
        if not ready:
            raise RuntimeError("kubectl port-forward for Elasticsearch did not become ready")
        yield forwarded_url
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


def _run_sync_with_count(argv: list[str] | None) -> tuple[int, int]:
    """Returns ``(exit_code, synced_document_count)``.

    Exit code follows shell conventions: ``0`` success, ``1`` validation or sync failure.
    ``synced_document_count`` is ``0`` when exit code is non-zero.
    """
    args = _parse_args(argv)
    if not args.project_id:
        _log("ERROR: --project-id / PROJECT_ID is required")
        return (1, 0)
    if not args.es_url:
        _log(
            "ERROR: --es-url / ELASTICSEARCH_URL is empty "
            "(e.g. http://elasticsearch.search.svc.cluster.local:9200)"
        )
        return (1, 0)

    fq_table = args.table
    if "." in fq_table and fq_table.count(".") == 1:
        fq_table = f"{args.project_id}.{args.table}"

    _log(f"STEP 1 — BQ load table={fq_table}")
    bq = bigquery.Client(project=args.project_id)
    rows = load_properties_cleaned_rows(client=bq, fq_table=fq_table)
    if not rows:
        _log("no rows to sync; returning 0")
        return (0, 0)

    base = args.es_url.rstrip("/")
    hdrs = _headers(api_key=args.api_key)
    auth: tuple[str, str] | None = None
    if not args.api_key and args.username and args.password:
        auth = (args.username, args.password)

    _log(f"STEP 2 — bulk upsert index={args.index} rows={len(rows)} url={base}")
    with _maybe_port_forward_for_cluster_dns(base) as resolved_base:
        _log(f"STEP 2.1 — resolved Elasticsearch url={resolved_base}")
        host = urlparse(resolved_base).hostname or ""
        verify_tls = host not in {"127.0.0.1", "localhost"}
        with httpx.Client(timeout=120.0, verify=verify_tls, auth=auth) as client:
            _ensure_index(client=client, base=resolved_base, index=args.index, headers=hdrs)
            _bulk_upsert(
                client=client,
                base=resolved_base,
                index=args.index,
                rows=rows,
                headers=hdrs,
                batch_size=args.batch_size,
            )

    _log(f"DONE upserted {len(rows)} documents")
    return (0, len(rows))


def run(argv: list[str] | None = None) -> int:
    """Shell-style exit code for programmatic callers (e.g. deploy-all step runner).

    **Contract**: ``0`` = success, non-zero = failure. Document counts are not encoded here
    (previously ``run`` returned ``len(rows)``, which made ``rc >= 0`` look like success for
    validation failures that returned ``1``).
    """
    code, _count = _run_sync_with_count(argv)
    return code


def main(argv: list[str] | None = None) -> int:
    try:
        code, count = _run_sync_with_count(argv)
    except Exception as exc:
        _log(f"UNCAUGHT EXCEPTION: {exc}")
        _log(traceback.format_exc())
        print(f"sync_failed={exc}")
        return 1
    if code == 0:
        print(f"synced_documents={count}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
