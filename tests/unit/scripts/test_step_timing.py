"""``scripts.lib.step_timing`` — shared per-step wall-clock history (CSV) + ETA.

Used by deploy-all / destroy-all / run-all so the "is it stuck?" judgment has a
baseline instead of a guess. These tests pin the CSV format, the median-of-ok
baseline logic, and the ETA output (including the lower-bound case when some
steps have no history yet).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.lib import step_timing


@pytest.fixture(autouse=True)
def _isolate_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(step_timing, "CSV_PATH", tmp_path / "step_timings.csv")


def test_fmt_duration_human_readable() -> None:
    assert step_timing.fmt_duration(45) == "45s"
    assert step_timing.fmt_duration(572) == "9m32s"
    assert step_timing.fmt_duration(3490) == "58m10s"
    assert step_timing.fmt_duration(3600) == "1h00m"
    assert step_timing.fmt_duration(0) == "0s"
    assert step_timing.fmt_duration(-3) == "0s"


def test_record_writes_header_then_rows_and_baselines_use_median_of_ok_runs() -> None:
    step_timing.record("deploy-all", 6, "tf-apply", 3490.0, "ok")
    step_timing.record("deploy-all", 6, "tf-apply", 3500.0, "ok")
    step_timing.record("deploy-all", 7, "seed-lgbm-model", 8.0, "ok")
    step_timing.record("deploy-all", 5, "tf-plan", 999.0, "failed")  # must not feed the baseline
    step_timing.record("destroy-all", 1, "tf-apply", 11.0, "ok")  # different flow → separate

    rows = step_timing.CSV_PATH.read_text(encoding="utf-8").splitlines()
    assert rows[0] == ",".join(step_timing.HEADER)
    assert len(rows) == 1 + 5  # header + 5 data rows

    base = step_timing.baselines("deploy-all")
    assert base["tf-apply"] == 3495.0  # median of [3490, 3500] — destroy-all's 11.0 excluded
    assert base["seed-lgbm-model"] == 8.0
    assert "tf-plan" not in base  # only status == "ok" rows count

    assert step_timing.baselines("destroy-all")["tf-apply"] == 11.0
    assert step_timing.baselines("run-all") == {}  # no rows for that flow


def test_record_keeps_only_recent_runs_per_step_for_the_median() -> None:
    # KEEP_PER_STEP=10 by default; with an old slow run plus 10 fast ones the
    # median should reflect only the recent window, not the stale outlier.
    step_timing.record("run-all", 1, "ops-search", 999.0, "ok")
    for _ in range(step_timing.KEEP_PER_STEP):
        step_timing.record("run-all", 1, "ops-search", 5.0, "ok")
    assert step_timing.baselines("run-all")["ops-search"] == 5.0


def test_record_is_best_effort_and_never_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    # Point at an unwritable path (a file used as a directory) → record() must swallow OSError.
    bad = step_timing.CSV_PATH.parent / "blocker"
    bad.write_text("x")
    monkeypatch.setattr(step_timing, "CSV_PATH", bad / "nested" / "step_timings.csv")
    step_timing.record("deploy-all", 1, "x", 1.0, "ok")  # must not raise
    assert step_timing.baselines("deploy-all") == {}  # unreadable → empty, still no raise


def test_print_eta_no_history(capsys: pytest.CaptureFixture[str]) -> None:
    step_timing.print_eta("deploy-all", ["alpha", "beta"])
    assert "no prior timing history" in capsys.readouterr().out


def test_print_eta_sums_known_step_baselines(capsys: pytest.CaptureFixture[str]) -> None:
    step_timing.record("deploy-all", 1, "alpha", 10.0, "ok")
    step_timing.record("deploy-all", 2, "beta", 3500.0, "ok")
    # gamma has no history → estimate becomes a lower bound (≥), gamma surfaced as missing.
    step_timing.print_eta("deploy-all", ["alpha", "beta", "gamma"])
    out = capsys.readouterr().out
    assert "deploy-all ETA" in out
    assert "≥" in out, "estimate must be a lower bound when some steps lack history"
    assert "beta=58m" in out, "the heaviest step must be surfaced"
    assert "no history yet for: gamma" in out


def test_print_eta_all_known_uses_tilde_prefix(capsys: pytest.CaptureFixture[str]) -> None:
    step_timing.record("destroy-all", 1, "a", 30.0, "ok")
    step_timing.record("destroy-all", 2, "b", 90.0, "ok")
    step_timing.print_eta("destroy-all", ["a", "b"])
    out = capsys.readouterr().out
    assert "~2m" in out  # 30 + 90 = 120s → ~2m00s
    assert "≥" not in out
