"""Shared helper for ``scripts.verify.*`` modules.

Replaces the multi-line ``bash -c '...| tee'`` blocks that used to live
inline in the Makefile (``verify-deploy-all`` / ``verify-destroy-all`` /
``verify-live-acceptance`` / ``verify-full-recreate``) with a single
Python entry point that always behaves the same.
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_log_dir() -> Path:
    """Match the Makefile default ``$(VERIFY_LOG_DIR) = $(LOG_ROOT)/verification``.

    Honour ``VERIFY_LOG_DIR`` when set, otherwise compose from
    ``LOG_ROOT`` (default ``<repo_root>/logs``) so subprocess invocations
    from the Makefile keep using the same path.
    """
    explicit = os.environ.get("VERIFY_LOG_DIR")
    if explicit:
        return Path(explicit)
    log_root = os.environ.get("LOG_ROOT") or str(_REPO_ROOT / "logs")
    return Path(log_root) / "verification"


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _update_symlink(link: Path, target_name: str) -> None:
    """``ln -sfn`` equivalent — replace any existing symlink atomically."""
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(target_name)


def run(label: str, cmd: list[str], *, env: dict[str, str] | None = None) -> int:
    """Run ``cmd`` while teeing combined stdout/stderr to a timestamped log.

    Mirrors the legacy Makefile recipe:

    - log file:   ``<verify_log_dir>/<label>-<utc>.log``
    - exit file:  ``<verify_log_dir>/<label>-<utc>.exit.txt``
    - latest:     ``<verify_log_dir>/<label>.latest.log`` (symlink)
    - latest exit: ``<verify_log_dir>/<label>.latest.exit.txt`` (symlink)

    Returns ``cmd``'s exit code. Caller (``main`` in each wrapper module)
    is expected to ``raise SystemExit(rc)`` so ``make`` propagates it.
    """
    log_dir = _resolve_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)

    stamp = _utc_stamp()
    log_file = log_dir / f"{label}-{stamp}.log"
    exit_file = log_dir / f"{label}-{stamp}.exit.txt"
    latest_log = log_dir / f"{label}.latest.log"
    latest_exit = log_dir / f"{label}.latest.exit.txt"

    print(f"verification-log: {log_file}")
    sys.stdout.flush()

    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    merged_env.setdefault("PYTHONUNBUFFERED", "1")

    with log_file.open("w", encoding="utf-8", buffering=1) as sink:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=merged_env,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            sink.write(line)
        rc = proc.wait()

    exit_file.write_text(f"{rc}\n", encoding="utf-8")
    _update_symlink(latest_log, log_file.name)
    _update_symlink(latest_exit, exit_file.name)
    return rc
