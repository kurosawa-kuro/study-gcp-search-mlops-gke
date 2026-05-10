"""Run the full-recreate pytest gate (destroy-all → deploy-all → acceptance).

Mirrors the previous shell recipe:

    RUN_LIVE_GCP_FULL_RECREATE=1 uv run pytest \
        tests/e2e/test_full_recreate_gate.py \
        -m "live_gcp and full_recreate" -v -s

The gate is flaky (Vertex async deletion timing) and is therefore kept
as an opt-in target, separate from ``verify-live-acceptance``.
"""

from __future__ import annotations

from scripts.verify._runner import run


def main() -> int:
    cmd = [
        "uv",
        "run",
        "pytest",
        "tests/e2e/test_full_recreate_gate.py",
        "-m",
        "live_gcp and full_recreate",
        "-v",
        "-s",
    ]
    return run("full-recreate", cmd, env={"RUN_LIVE_GCP_FULL_RECREATE": "1"})


if __name__ == "__main__":
    raise SystemExit(main())
