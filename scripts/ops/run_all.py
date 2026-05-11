"""`run-all-core` as a Python step orchestrator (replaces the bash recipe).

Why a Python orchestrator:
  - **per-step timing**: each step's wall time is appended to logs/step_timings.csv
    (flow=run-all) via ``scripts.lib.step_timing``, and the run prints an ETA from
    the median of recent runs — symmetric with deploy-all / destroy-all.
  - **correct step ORDER**: the old recipe ran ``ops-train-now`` *before* any label
    generation, so the reranker's ``load_features`` got an empty ``ranking_labels``
    frame and ``train-reranker`` crashed ("Empty training frame ..."). Behavior
    seeding (``ops-label-seed``) + label materialization (``label-build``) now run
    BEFORE ``ops-train-now``. ``ops-livez`` / ``ops-search`` also move up so the
    KServe encoder is warm before the behavior posts hit ``/search``.

Same semantics as the old recipe otherwise: run each ``make <target>`` in order,
fail fast on the first non-zero. ``make run-all-core`` → ``uv run python -m scripts.ops.run_all``.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from scripts.lib import step_timing

# scripts/ops/run_all.py → repo root is parents[2] (scripts/ops, scripts, <root>).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_FLOW = "run-all"

# Order matters (see module docstring): readiness → search warmup → component
# checks → behavior seeding → label materialization → train → daily → accuracy.
STEPS: tuple[str, ...] = (
    "check-layers",
    "seed-test",
    "sync-elasticsearch",
    "ops-livez",
    "ops-search",
    "ops-search-components",
    "ops-vertex-vector-search-smoke",
    "ops-vertex-feature-group",
    "ops-feedback",
    "ops-ranking",
    "ops-label-seed",
    "label-build",
    "ops-train-now",
    "ops-train-wait",
    "ops-daily",
    "ops-accuracy-report",
)


def _run_make(target: str) -> int:
    return subprocess.run(["make", target], cwd=_REPO_ROOT, check=False).returncode


def main() -> int:
    total = len(STEPS)
    print(f"==> run-all-core: {total} step(s) — {list(STEPS)}")
    step_timing.print_eta(_FLOW, list(STEPS))
    overall = time.monotonic()
    for i, target in enumerate(STEPS, start=1):
        print()
        print("================================================================")
        print(f" run-all  step {i}/{total}: {target}")
        if i > 1:
            print(f" (total_elapsed={time.monotonic() - overall:.0f}s)")
        print("================================================================")
        t0 = time.monotonic()
        rc = _run_make(target)
        elapsed = time.monotonic() - t0
        if rc != 0:
            step_timing.record(_FLOW, i, target, elapsed, "failed")
            print(f"==> run-all-core FAILED at step {i} ({target}) — see logs above")
            return rc
        print(f" run-all  step-done elapsed={elapsed:.0f}s")
        step_timing.record(_FLOW, i, target, elapsed, "ok")
    total_elapsed = time.monotonic() - overall
    print()
    print(
        f"==> run-all-core complete. total_elapsed={total_elapsed:.0f}s "
        f"({step_timing.fmt_duration(total_elapsed)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
