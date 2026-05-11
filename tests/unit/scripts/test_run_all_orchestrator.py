"""``scripts.ops.run_all`` — the run-all-core step orchestrator.

Pins the canonical validation step list + order (the 2026-05-11 incident: the
old bash recipe ran ``ops-train-now`` before any label generation, so the
reranker's ``load_features`` got an empty ``ranking_labels`` frame and
``train-reranker`` crashed) and the fail-fast / per-step-timing behaviour.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.lib import step_timing
from scripts.ops import run_all


@pytest.fixture(autouse=True)
def _isolate_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(step_timing, "CSV_PATH", tmp_path / "step_timings.csv")


def test_steps_are_the_canonical_validation_sequence() -> None:
    assert list(run_all.STEPS) == [
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
    ]
    # incident-derived invariant: behavior seeding + ranking_labels materialization
    # must precede ops-train-now (else train-reranker gets an empty training frame).
    assert run_all.STEPS.index("ops-label-seed") < run_all.STEPS.index("ops-train-now")
    assert run_all.STEPS.index("label-build") < run_all.STEPS.index("ops-train-now")
    # sync-elasticsearch must precede the search smokes (lexical lane must be populated).
    assert run_all.STEPS.index("sync-elasticsearch") < run_all.STEPS.index("ops-search")


def test_main_runs_every_step_in_order_then_records_ok() -> None:
    calls: list[str] = []

    def _fake_run(cmd: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(cmd[1])  # ["make", <target>]
        return subprocess.CompletedProcess(cmd, returncode=0)

    with patch("scripts.ops.run_all.subprocess.run", side_effect=_fake_run):
        rc = run_all.main()

    assert rc == 0
    assert calls == list(run_all.STEPS)
    base = step_timing.baselines("run-all")
    # every step recorded an "ok" timing row
    assert set(base) == set(run_all.STEPS)


def test_main_fails_fast_on_first_nonzero_step() -> None:
    calls: list[str] = []

    def _fake_run(cmd: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        target = cmd[1]
        calls.append(target)
        return subprocess.CompletedProcess(cmd, returncode=7 if target == "ops-train-now" else 0)

    with patch("scripts.ops.run_all.subprocess.run", side_effect=_fake_run):
        rc = run_all.main()

    assert rc == 7
    # stopped at ops-train-now — nothing after it ran
    assert calls[-1] == "ops-train-now"
    assert "ops-train-wait" not in calls
    base = step_timing.baselines("run-all")
    assert "ops-train-now" not in base  # the failing step is recorded as "failed", not "ok"
    assert "ops-label-seed" in base  # the step before it succeeded


def test_makefile_run_all_core_delegates_to_orchestrator() -> None:
    makefile = (Path(__file__).resolve().parents[3] / "Makefile").read_text(encoding="utf-8")
    assert "run-all-core:" in makefile
    assert "uv run python -u -m scripts.ops.run_all" in makefile
