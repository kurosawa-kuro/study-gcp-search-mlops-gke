"""Run the live GCP acceptance pytest gate against an existing deploy.

Mirrors the previous shell recipe:

    RUN_LIVE_GCP_ACCEPTANCE=1 uv run pytest \
        tests/e2e/test_live_acceptance_gate.py -m live_gcp -v -s

Logs go to ``logs/verification/live-acceptance-<utc>.log`` with
``live-acceptance.latest.log`` symlink kept fresh.
"""

from __future__ import annotations

from scripts.verify._runner import run


def main() -> int:
    cmd = [
        "uv",
        "run",
        "pytest",
        "tests/e2e/test_live_acceptance_gate.py",
        "-m",
        "live_gcp",
        "-v",
        "-s",
    ]
    return run("live-acceptance", cmd, env={"RUN_LIVE_GCP_ACCEPTANCE": "1"})


if __name__ == "__main__":
    raise SystemExit(main())
