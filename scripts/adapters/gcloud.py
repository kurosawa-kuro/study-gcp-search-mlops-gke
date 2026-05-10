"""Thin adapter around the `gcloud` CLI.

Centralizes gcloud invocations introduced 2026-05-10 (M-Wave8.6 Phase 3,
sibling: `scripts/adapters/kubectl.py`, `scripts/adapters/terraform.py`).

Signature is unified across the three adapters: each returns a
`subprocess.CompletedProcess[str]` so callers can inspect `.stdout`,
`.stderr`, `.returncode` consistently.

Migration note (2026-05-10):
- The legacy helper `scripts/_common.py::gcloud(*args, capture) -> str`
  returned a stripped stdout string (different shape). Existing callers using
  `from scripts._common import gcloud` continue to work, but new callers
  should use `gcloud_run(...)` (this module).
"""

from __future__ import annotations

import subprocess

from scripts._common import run as _run


def gcloud_run(
    *args: str,
    capture: bool = False,
    check: bool = True,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    """Invoke `gcloud <args...>`. Returns the completed subprocess.

    Examples:
        gcloud_run("services", "enable", "--project=mlops-dev-a", "iam.googleapis.com")
        proc = gcloud_run("ai", "indexes", "list", "--region=asia-northeast1", capture=True)
        # proc.stdout has the JSON / table output, proc.returncode for status
    """
    return _run(["gcloud", *args], capture=capture, check=check, timeout=timeout)
