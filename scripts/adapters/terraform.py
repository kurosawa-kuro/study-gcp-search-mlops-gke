"""Thin adapter around the `terraform` CLI.

Centralizes terraform invocations introduced 2026-05-10 (M-Wave8.6 Phase 3,
sibling: `scripts/adapters/kubectl.py`, `scripts/adapters/gcloud.py`).

Why a wrapper:
- Single mock target avoids 2026-05-10 incident pattern (mock 漏れ → real CLI hang)
- `-chdir` is universally needed for terraform commands; passing as kwarg is
  cleaner than threading through every caller's argv construction
- For state-lock-aware retry, callers should still use
  `scripts.domain.terraform.lock.run_terraform_streaming_with_lock_retry`. This
  adapter is for one-shot calls (plan, output, state list/rm/import).
"""

from __future__ import annotations

import subprocess

from scripts._common import run as _run


def terraform_run(
    *args: str,
    chdir: str | None = None,
    capture: bool = False,
    check: bool = True,
    timeout: int | None = None,
    input: str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Invoke `terraform [-chdir=...] <args...>`. Returns the completed subprocess.

    Examples:
        terraform_run("init", chdir=str(INFRA))
        terraform_run("output", "-json", chdir=str(INFRA), capture=True)
        terraform_run("state", "list", chdir=str(INFRA), capture=True)
        terraform_run("state", "list", chdir=str(INFRA), env={"TF_VAR_x": "y"})
    """
    cmd = ["terraform"]
    if chdir is not None:
        cmd.append(f"-chdir={chdir}")
    cmd.extend(args)
    return _run(cmd, capture=capture, check=check, timeout=timeout, input=input, env=env)
