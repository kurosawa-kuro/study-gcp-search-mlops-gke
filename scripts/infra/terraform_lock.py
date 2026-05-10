"""Terraform remote state lock detection and optional one-shot recovery.

Remote backends (e.g. GCS ``default.tflock``) reject concurrent operations.
``destroy-all`` / ``deploy-all`` / interrupted CI can leave a stale lock if a
process died mid-apply. Auto-unlock is **dangerous** if another legitimate
``terraform apply`` is running — recovery is opt-in via ``TERRAFORM_STATE_FORCE_UNLOCK``
(aliases: ``DESTROY_ALL_FORCE_UNLOCK``, ``DEPLOY_ALL_FORCE_UNLOCK``).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

# Terraform CLI wraps the lock info table in box-drawing characters (``│``) and
# ANSI color codes (``\x1b[31m`` etc.). The 2026-05-10 incident showed that the
# original anchor ``^\s*ID:`` did not match these prefixes — a stale lock could
# not be parsed even when ``TERRAFORM_STATE_FORCE_UNLOCK=1`` was set, so the
# auto-recovery silently fell back to "lock ID missing — cannot force-unlock".
# Fix: strip ANSI first, then anchor on a relaxed line prefix that allows any
# non-alphanumeric characters (whitespace + ``│`` + residual ANSI bytes).
_ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
_LOCK_ID_RE = re.compile(r"^[^A-Za-z0-9]*ID:\s+(\d+)\s*$", re.MULTILINE)

# Opt-in for stale locks only. Checked in order; first set wins.
_UNLOCK_ENV_NAMES = (
    "TERRAFORM_STATE_FORCE_UNLOCK",
    "DESTROY_ALL_FORCE_UNLOCK",
    "DEPLOY_ALL_FORCE_UNLOCK",
)


def should_auto_force_unlock() -> bool:
    """True if user opted in to ``terraform force-unlock`` for a stale lock."""
    for name in _UNLOCK_ENV_NAMES:
        raw = os.environ.get(name, "").strip().lower()
        if raw in {"1", "true", "yes", "on"}:
            return True
    return False


def parse_terraform_lock_id(combined_output: str) -> str | None:
    """Parse the lock ID from terraform's ``Error acquiring the state lock`` output.

    Strips ANSI color codes before matching so the regex anchor works on lines
    like ``\\x1b[31m│\\x1b[0m   ID:   1778332028753123`` (terraform CLI default
    color output, observed 2026-05-10).
    """
    cleaned = _ANSI_ESCAPE_RE.sub("", combined_output)
    m = _LOCK_ID_RE.search(cleaned)
    return m.group(1) if m else None


def is_state_lock_error(combined_output: str) -> bool:
    return "Error acquiring the state lock" in combined_output


def run_terraform_streaming_with_lock_retry(
    cmd: list[str],
    *,
    chdir_infra: Path,
) -> None:
    """Run ``terraform`` with stdout streamed; on state-lock error print help or unlock+retry.

    When auto-unlock is enabled (see ``should_auto_force_unlock``) and lock ID
    is parsed, runs ``terraform force-unlock -force <id>`` then retries ``cmd`` once.
    """
    rc, full_output = _run_stream_capture(cmd)
    if rc == 0:
        return
    if not is_state_lock_error(full_output):
        raise subprocess.CalledProcessError(rc, cmd, full_output, None)

    lock_id = parse_terraform_lock_id(full_output)
    print(
        "\n==> Terraform remote state is locked (another apply/destroy may be running).\n"
        f"    Parsed lock ID: {lock_id or '(could not parse — see terraform output above)'}\n"
        "    Safe fix: wait for the other process to finish.\n"
        "    Manual unlock (only if nothing else uses this state):\n"
        f"      terraform -chdir={chdir_infra} force-unlock -force <LOCK_ID>\n"
        "    Automated retry: set TERRAFORM_STATE_FORCE_UNLOCK=1 and re-run "
        "(same caveat).\n",
        flush=True,
        file=sys.stderr,
    )
    if not should_auto_force_unlock():
        raise SystemExit(1)
    if not lock_id:
        print(
            "==> auto force-unlock enabled but lock ID missing — cannot force-unlock.",
            file=sys.stderr,
            flush=True,
        )
        raise SystemExit(1)

    unlock_cmd = [
        "terraform",
        f"-chdir={chdir_infra}",
        "force-unlock",
        "-force",
        lock_id,
    ]
    print(f"==> TERRAFORM_STATE_FORCE_UNLOCK — {' '.join(unlock_cmd)}", flush=True)
    subprocess.run(unlock_cmd, check=True)
    print("==> retrying terraform command once after force-unlock\n", flush=True)
    rc2, _ = _run_stream_capture(cmd)
    if rc2 != 0:
        raise subprocess.CalledProcessError(rc2, cmd)


def _run_stream_capture(cmd: list[str]) -> tuple[int, str]:
    """Stream stdout+stderr to terminal while capturing for lock parsing."""
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    chunks: list[str] = []
    assert p.stdout is not None
    for line in p.stdout:
        chunks.append(line)
        print(line, end="", flush=True)
    return p.wait(), "".join(chunks)
