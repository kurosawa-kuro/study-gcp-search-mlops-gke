"""Composer DAG ``trigger`` / ``list-runs`` wrapper.

Replaces the multi-line ``gcloud composer environments run ... \\``
recipes that used to live inline in the Makefile (``ops-composer-trigger``
/ ``ops-composer-list-runs``). One ``uv run python -m
scripts.ops.composer_dag <subcmd>`` call covers both.

Both subcommands require ``DAG`` (positional or ``--dag``) so the
Makefile can stay a thin 1-line wrapper while keeping the same UX:

    make ops-composer-trigger DAG=retrain_orchestration
    make ops-composer-list-runs DAG=retrain_orchestration
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def _resolve(name: str, default: str = "") -> str:
    return os.environ.get(name, "").strip() or default


def _build_gcloud_cmd(
    subcmd: str, *, env_name: str, project_id: str, region: str, dag: str
) -> list[str]:
    base = [
        "gcloud",
        "composer",
        "environments",
        "run",
        env_name,
        f"--project={project_id}",
        f"--location={region}",
    ]
    if subcmd == "trigger":
        return [*base, "dags", "trigger", "--", dag]
    if subcmd == "list-runs":
        return [*base, "dags", "list-runs", "--", "--dag-id", dag]
    raise ValueError(f"unknown subcommand: {subcmd}")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "subcommand",
        choices=["trigger", "list-runs"],
        help="Composer DAG subcommand",
    )
    parser.add_argument(
        "--dag",
        default=os.environ.get("DAG", ""),
        help="DAG id. Defaults to $DAG env var (set via `make ops-composer-* DAG=<id>`).",
    )
    parser.add_argument(
        "--composer-env",
        default=_resolve("COMPOSER_ENV", "hybrid-search-orchestrator"),
    )
    parser.add_argument(
        "--project-id",
        default=_resolve("PROJECT_ID", "mlops-dev-a"),
    )
    parser.add_argument(
        "--region",
        default=_resolve("REGION", "asia-northeast1"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if not args.dag:
        print(
            f"Usage: make ops-composer-{args.subcommand} DAG=<dag_id>",
            file=sys.stderr,
        )
        return 1
    cmd = _build_gcloud_cmd(
        args.subcommand,
        env_name=args.composer_env,
        project_id=args.project_id,
        region=args.region,
        dag=args.dag,
    )
    proc = subprocess.run(cmd, check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
