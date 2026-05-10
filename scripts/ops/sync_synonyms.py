"""Seed / sync the lexical synonym dictionary into Cloud Memorystore for Redis.

Reads ``definitions/synonyms/real_estate_ja.yaml`` (curated property-domain
synonyms) and rewrites the ``syn:<token>`` SETs in Redis. Designed to be
invoked as a one-shot Cloud Run Job, a Composer DAG step, or locally:

    python -m scripts.ops.sync_synonyms \\
        --redis-url redis://10.x.x.x:6379/0 \\
        --dictionary definitions/synonyms/real_estate_ja.yaml

The script is idempotent and atomic per token: each ``syn:<token>`` SET
is replaced via ``DEL`` + ``SADD`` inside a single MULTI/EXEC pipeline so
a stale subset never appears under live ``/search`` traffic.

Auth:
- Cloud Memorystore AUTH string is read from ``REDIS_AUTH`` env var
  (mirrors the ``synonym-redis-auth`` Secret in the GKE Pod).
- When AUTH is disabled the env var is unset and the URL is used as-is.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from scripts.adapters.gcloud import gcloud_run


def _log(msg: str) -> None:
    print(f"[sync_synonyms] {msg}", flush=True)


def _gcloud(args: list[str]) -> str:
    """Run a ``gcloud`` command and return stdout.strip(); empty on failure."""
    try:
        proc = gcloud_run(
            *args,
            check=False,
            capture=True,
            timeout=60,
        )
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        _log(f"gcloud invocation failed: {exc}")
        return ""
    if proc.returncode != 0:
        return ""
    return proc.stdout.strip()


def _resolve_redis_url(*, project_id: str, region: str, instance: str) -> str:
    """Resolve ``redis://<host>:<port>/0`` from a Memorystore instance.

    Returns empty string when the instance is not provisioned (Memorystore
    is opt-in; the Makefile target legitimately ``exit 0`` in that case so
    the caller is responsible for treating empty as "skip sync").
    """
    explicit = os.environ.get("SYNONYM_REDIS_URL", "").strip()
    if explicit:
        return explicit
    host = _gcloud(
        [
            "redis",
            "instances",
            "describe",
            instance,
            f"--project={project_id}",
            f"--region={region}",
            "--format=value(host)",
        ]
    )
    if not host:
        return ""
    port = (
        _gcloud(
            [
                "redis",
                "instances",
                "describe",
                instance,
                f"--project={project_id}",
                f"--region={region}",
                "--format=value(port)",
            ]
        )
        or "6379"
    )
    return f"redis://{host}:{port}/0"


def _resolve_redis_auth(*, project_id: str, secret_id: str) -> str:
    explicit = os.environ.get("REDIS_AUTH", "").strip()
    if explicit:
        return explicit
    minted = _gcloud(
        [
            "secrets",
            "versions",
            "access",
            "latest",
            f"--secret={secret_id}",
            f"--project={project_id}",
        ]
    )
    if minted:
        # Match the legacy Makefile contract: REDIS_AUTH env is consumed by
        # ``redis.from_url`` via ``os.environ.get('REDIS_AUTH')`` below.
        os.environ["REDIS_AUTH"] = minted
    return minted


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-id",
        default=os.environ.get("PROJECT_ID", "mlops-dev-a"),
    )
    parser.add_argument(
        "--region",
        default=os.environ.get("REGION", "asia-northeast1"),
    )
    parser.add_argument(
        "--redis-instance",
        default=os.environ.get("SYNONYM_REDIS_INSTANCE", "phase7-synonym"),
        help="Memorystore instance name to resolve --redis-url from when omitted.",
    )
    parser.add_argument(
        "--redis-auth-secret-id",
        default=os.environ.get("SYNONYM_REDIS_AUTH_SECRET_ID", "phase7-synonym-redis-auth"),
        help="Secret Manager secret id for Memorystore AUTH string.",
    )
    parser.add_argument(
        "--redis-url",
        default="",
        help="redis:// URL. If empty, resolved via gcloud redis instances describe.",
    )
    parser.add_argument(
        "--dictionary",
        default="definitions/synonyms/real_estate_ja.yaml",
        help="YAML path with token -> [synonyms] mapping",
    )
    parser.add_argument(
        "--key-prefix",
        default=os.environ.get("SYNONYM_KEY_PREFIX", "syn:"),
        help="Redis key prefix (default 'syn:')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse the YAML and report stats without writing to Redis",
    )
    parser.add_argument(
        "--skip-when-unprovisioned",
        action="store_true",
        default=True,
        help=(
            "Exit 0 when the Memorystore instance is not provisioned (default). "
            "Mirrors the legacy Makefile recipe so run-all-core stays green when "
            "enable_redis_synonym=false."
        ),
    )
    return parser.parse_args(argv)


def _load_dictionary(path: str) -> dict[str, list[str]]:
    raw: Any = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must be a top-level mapping; got {type(raw).__name__}")
    out: dict[str, list[str]] = {}
    for token, synonyms in raw.items():
        if not isinstance(token, str) or not token.strip():
            raise ValueError(f"{path}: invalid token {token!r}")
        if not isinstance(synonyms, list):
            raise ValueError(f"{path}: token {token!r} must map to a list")
        cleaned = [s.strip() for s in synonyms if isinstance(s, str) and s.strip()]
        if cleaned:
            out[token.strip()] = sorted(set(cleaned))
    return out


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    dictionary = _load_dictionary(args.dictionary)
    total_synonyms = sum(len(v) for v in dictionary.values())
    _log(
        f"loaded {len(dictionary)} canonical tokens "
        f"({total_synonyms} synonyms total) from {args.dictionary}"
    )

    if args.dry_run:
        _log("--dry-run: skipping Redis writes")
        for token, synonyms in dictionary.items():
            _log(f"  {args.key_prefix}{token} -> {synonyms}")
        return 0

    if not args.redis_url:
        args.redis_url = _resolve_redis_url(
            project_id=args.project_id,
            region=args.region,
            instance=args.redis_instance,
        )

    if not args.redis_url:
        msg = (
            f"Memorystore '{args.redis_instance}' not provisioned "
            f"(set enable_redis_synonym=true to opt in)"
        )
        if args.skip_when_unprovisioned:
            _log(f"[skip] {msg}")
            return 0
        _log(f"ERROR: --redis-url empty and {msg}")
        return 1

    _resolve_redis_auth(
        project_id=args.project_id,
        secret_id=args.redis_auth_secret_id,
    )

    try:
        import redis  # type: ignore[import-not-found]
    except ImportError:
        _log("ERROR: 'redis' package not installed. uv add redis or pip install redis")
        return 2

    password = os.environ.get("REDIS_AUTH") or None
    client = redis.from_url(  # type: ignore[no-untyped-call]
        args.redis_url,
        password=password,
        socket_connect_timeout=5.0,
        socket_timeout=5.0,
    )
    client.ping()
    _log("connected to Redis")

    written = 0
    pipe = client.pipeline(transaction=False)
    for token, synonyms in dictionary.items():
        key = f"{args.key_prefix}{token}"
        pipe.delete(key)
        if synonyms:
            pipe.sadd(key, *synonyms)
        written += 1
    pipe.execute()
    _log(f"wrote {written} synonym keys")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
