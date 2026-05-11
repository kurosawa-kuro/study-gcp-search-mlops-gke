"""Per-step wall-clock history for the long flows (deploy-all / destroy-all / run-all).

Every completed step appends one row to ``logs/step_timings.csv`` (gitignored,
machine-local). At the start of a run the orchestrator reads it back and prints
an ETA derived from the **median of recent successful runs on this host** — so
"is it stuck?" is judged against a baseline instead of a guess (cf. the 58 min
deploy-all step 6 incident, where the silent terraform apply looked frozen).

The CSV carries a ``flow`` column so deploy-all / destroy-all / run-all keep
separate baselines from one file. Single source of truth — `deploy_all.py`,
`destroy_all.py` and `scripts/ops/run_all.py` all funnel through here so the
format / median logic cannot drift between flows.
"""

from __future__ import annotations

import csv
import datetime as _dt
import statistics
from pathlib import Path

# Repo root: scripts/lib/step_timing.py → parents[0]=scripts/lib, [1]=scripts, [2]=<root>.
_REPO_ROOT = Path(__file__).resolve().parents[2]

# Module-level so tests can monkeypatch it to a tmp path.
CSV_PATH = _REPO_ROOT / "logs" / "step_timings.csv"
HEADER = ("recorded_at_utc", "flow", "step_number", "step_name", "elapsed_sec", "status")
KEEP_PER_STEP = 10  # median over the most recent N successful runs per (flow, step)
MAX_ROWS = 8000  # soft cap; oldest data rows trimmed on append


def fmt_duration(sec: float) -> str:
    """Human-readable duration: ``45s`` / ``9m32s`` / ``1h02m``."""
    total = max(0, round(sec))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"


def record(flow: str, step_number: int, step_name: str, elapsed_sec: float, status: str) -> None:
    """Append one timing row. Best-effort — never raises (timing is a convenience)."""
    try:
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        new_file = not CSV_PATH.exists()
        row = [
            _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            flow,
            str(step_number),
            step_name,
            f"{elapsed_sec:.1f}",
            status,
        ]
        with CSV_PATH.open("a", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            if new_file:
                writer.writerow(HEADER)
            writer.writerow(row)
        _trim()
    except OSError:
        pass


def _trim() -> None:
    try:
        with CSV_PATH.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        if len(rows) <= MAX_ROWS + 1:  # +1 for the header row
            return
        with CSV_PATH.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(rows[0])
            writer.writerows(rows[1:][-MAX_ROWS:])
    except OSError:
        pass


def baselines(flow: str) -> dict[str, float]:
    """Median elapsed-seconds per step name over recent ``status == "ok"`` rows for ``flow``."""
    samples: dict[str, list[float]] = {}
    try:
        if not CSV_PATH.exists():
            return {}
        with CSV_PATH.open(newline="", encoding="utf-8") as fh:
            for rec in csv.DictReader(fh):
                if rec.get("flow") != flow or rec.get("status") != "ok":
                    continue
                name = rec.get("step_name") or ""
                try:
                    samples.setdefault(name, []).append(float(rec.get("elapsed_sec") or 0.0))
                except ValueError:
                    continue
    except OSError:
        return {}
    return {
        name: statistics.median(vals[-KEEP_PER_STEP:]) for name, vals in samples.items() if vals
    }


def print_eta(flow: str, step_names: list[str]) -> None:
    """Print an ETA line (+ heaviest steps) for ``step_names`` from the recorded history."""
    base = baselines(flow)
    if not base:
        print(
            f"==> {flow} ETA: no prior timing history yet ({CSV_PATH.name}) — this run will seed it"
        )
        return
    known = [base[name] for name in step_names if name in base]
    missing = [name for name in step_names if name not in base]
    prefix = "~" if not missing else "≥"
    print(
        f"==> {flow} ETA: {prefix}{fmt_duration(sum(known))} for {len(step_names)} step(s) "
        f"(median of recent runs; {len(known)}/{len(step_names)} steps have history)"
    )
    heavy = sorted(
        ((name, base[name]) for name in step_names if name in base),
        key=lambda kv: kv[1],
        reverse=True,
    )[:3]
    if heavy:
        print("    biggest: " + ", ".join(f"{name}={fmt_duration(sec)}" for name, sec in heavy))
    if missing:
        print(f"    no history yet for: {', '.join(missing)}")
