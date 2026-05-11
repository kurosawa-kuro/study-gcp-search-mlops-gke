"""Per-step timing in ``scripts.setup.deploy_all``.

When ``make deploy-all`` hangs in production, operators need to know WHICH
step is slow. The ``_step`` + ``_step_done`` helpers emit elapsed-time anchors
that ``scripts.deploy.monitor`` parses + operators grep in raw logs. These
tests pin the emitted line format so refactors don't silently break both
consumers.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts.setup import deploy_all as dall


@pytest.fixture(autouse=True)
def _reset_globals(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    dall._DEPLOY_ALL_STARTED_AT = None
    dall._STEP_STARTED_AT = None
    # Isolate the step-timing history CSV so `main()` / `_step_done()` in these
    # tests never touch the real logs/deploy_timings.csv.
    monkeypatch.setattr(dall, "_TIMINGS_CSV", tmp_path / "deploy_timings.csv")


def test_step_first_call_emits_header_without_elapsed_anchor(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Step 1 has no "prev_step_elapsed" / "total_elapsed" line because there
    is no previous step to anchor against."""
    dall._step(1, 7, "tf-bootstrap")
    out = capsys.readouterr().out
    assert "step 1/7: tf-bootstrap" in out
    assert "prev_step_elapsed" not in out, (
        "Step 1 must not emit prev_step_elapsed (there is no previous step)."
    )


def test_step_subsequent_calls_emit_elapsed_anchor(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Steps 2..N must emit prev_step_elapsed= + total_elapsed= so operators
    can see WHICH step is slow when they tail the log. Simulated clock jumps
    from t=100 (step 1 start) to t=300 (step 2 start) → prev elapsed 200s.
    """
    # Drive the module-level monotonic clock for both step entries so the
    # arithmetic is deterministic regardless of wall-clock drift.
    with patch("scripts.setup.deploy_all.time.monotonic", side_effect=[100.0, 300.0]):
        dall._step(1, 3, "first")
        dall._step(2, 3, "second")
    out = capsys.readouterr().out
    assert "step 2/3: second" in out
    anchor = re.search(r"prev_step_elapsed=(\d+)s\s+total_elapsed=(\d+)s", out)
    assert anchor is not None, f"Missing elapsed anchor in step 2 output:\n{out}"
    assert anchor.group(1) == "200", f"prev_step_elapsed should be 200s, got {anchor.group(1)}"
    assert anchor.group(2) == "200", f"total_elapsed should be 200s, got {anchor.group(2)}"


def test_step_done_emits_elapsed_line_matching_monitor_contract(
    capsys: pytest.CaptureFixture[str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """``scripts.deploy.monitor`` could in the future grep for
    ``deploy-all  step-done elapsed=<n>s``. Pin the exact prefix so refactors
    that change the spacing / label don't silently break log parsing.
    """
    monkeypatch.setattr(dall, "_TIMINGS_CSV", tmp_path / "deploy_timings.csv")
    step = dall.DeployStep(1, "tf-bootstrap", "tf-bootstrap", lambda: 0)
    dall._step(1, 2, "tf-bootstrap")
    dall._step_done(step)
    out = capsys.readouterr().out
    assert re.search(r"deploy-all\s+step-done\s+elapsed=\d+s", out), (
        f"step-done line missing or format changed:\n{out}"
    )


def test_step_done_noop_before_any_step() -> None:
    """Calling _step_done before any _step must be safe (no crash, no bogus
    "elapsed=4000000000s" from uninitialized monotonic baseline).
    """
    # No _step called → _STEP_STARTED_AT is None → _step_done silently no-ops.
    dall._step_done(dall.DeployStep(1, "x", "x", lambda: 0))  # must not raise


def test_fmt_duration_human_readable() -> None:
    assert dall._fmt_duration(45) == "45s"
    assert dall._fmt_duration(572) == "9m32s"
    assert dall._fmt_duration(3490) == "58m10s"
    assert dall._fmt_duration(3600) == "1h00m"
    assert dall._fmt_duration(0) == "0s"
    assert dall._fmt_duration(-3) == "0s"


def test_timing_history_records_rows_and_baselines_use_median_of_ok_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    csv_path = tmp_path / "deploy_timings.csv"
    monkeypatch.setattr(dall, "_TIMINGS_CSV", csv_path)

    dall._record_step_timing(6, "tf-apply", 3490.0, "ok")
    dall._record_step_timing(6, "tf-apply", 3500.0, "ok")
    dall._record_step_timing(7, "seed-lgbm-model", 8.0, "ok")
    dall._record_step_timing(5, "tf-plan", 999.0, "failed")  # must not feed the baseline

    # Human-readable CSV with the documented header.
    rows = csv_path.read_text(encoding="utf-8").splitlines()
    assert rows[0] == ",".join(dall._TIMINGS_HEADER)
    assert len(rows) == 1 + 4

    baselines = dall._load_step_baselines()
    assert baselines["tf-apply"] == 3495.0  # median of [3490, 3500]
    assert baselines["seed-lgbm-model"] == 8.0
    assert "tf-plan" not in baselines  # only status == "ok" rows count


def test_print_eta_sums_known_step_baselines(
    capsys: pytest.CaptureFixture[str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(dall, "_TIMINGS_CSV", tmp_path / "deploy_timings.csv")
    steps = [
        dall.DeployStep(1, "alpha", "alpha", lambda: 0),
        dall.DeployStep(2, "beta", "beta", lambda: 0),
        dall.DeployStep(3, "gamma", "gamma", lambda: 0),
    ]
    baselines = {"alpha": 10.0, "beta": 3500.0}  # gamma has no history
    dall._print_eta(steps, baselines)
    out = capsys.readouterr().out
    assert "deploy-all ETA" in out
    assert "≥" in out, "estimate must be a lower bound when some steps lack history"
    assert "beta=58m" in out  # heaviest step surfaced
    assert "no history yet for: gamma" in out


def test_print_eta_no_history(
    capsys: pytest.CaptureFixture[str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(dall, "_TIMINGS_CSV", tmp_path / "deploy_timings.csv")
    dall._print_eta([dall.DeployStep(1, "alpha", "alpha", lambda: 0)], {})
    assert "no prior timing history" in capsys.readouterr().out


def test_resolve_step_ref_accepts_number_and_name() -> None:
    steps = dall._steps()
    assert dall._resolve_step_ref("4", steps) == 4
    assert dall._resolve_step_ref("sync-dataform", steps) == 4


def test_main_honors_from_step_and_to_step(
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[str] = []

    def _runner(name: str):
        def _run() -> int:
            calls.append(name)
            return 0

        return _run

    steps = [
        dall.DeployStep(1, "one", "one", _runner("one")),
        dall.DeployStep(2, "two", "two", _runner("two")),
        dall.DeployStep(3, "three", "three", _runner("three")),
    ]

    with (
        patch(
            "scripts.setup.deploy_all._parse_args",
            return_value=type("Args", (), {"from_step": "2", "to_step": "3"})(),
        ),
        patch("scripts.setup.deploy_all._steps", return_value=steps),
    ):
        rc = dall.main()

    out = capsys.readouterr().out
    assert rc == 0
    assert calls == ["two", "three"]
    assert "from_step=2 to_step=3" in out


def test_main_prints_failure_summary_for_nonzero_step(
    capsys: pytest.CaptureFixture[str],
) -> None:
    steps = [
        dall.DeployStep(1, "one", "one", lambda: 0),
        dall.DeployStep(2, "broken", "broken", lambda: 7),
    ]

    with (
        patch(
            "scripts.setup.deploy_all._parse_args",
            return_value=type("Args", (), {"from_step": "1", "to_step": "2"})(),
        ),
        patch("scripts.setup.deploy_all._steps", return_value=steps),
    ):
        rc = dall.main()

    out = capsys.readouterr().out
    assert rc == 7
    assert "deploy-all FAILED at step 2 (broken)" in out


def test_run_tf_apply_uses_staged_apply_and_waits_for_readiness() -> None:
    stage1_calls: list[list[str]] = []
    stage2_calls: list[list[str]] = []

    def _fake_stage1(args: list[str], **_: object) -> None:
        stage1_calls.append(args)

    def _fake_stream(cmd: list[str], **_: object) -> None:
        stage2_calls.append(cmd)

    with (
        patch.dict(
            "os.environ",
            {
                "PROJECT_ID": "mlops-test",
                "REGION": "asia-northeast1",
                "GKE_CLUSTER_NAME": "hybrid-search",
                "VERTEX_VECTOR_SEARCH_DEPLOYED_INDEX_ID": "property_embeddings_v3",
            },
            clear=False,
        ),
        # 2026-05-09 refactor: tf-apply business logic は scripts.setup.tf_apply に
        # 分離。helper の mock patch も新所在へ追従する。
        patch(
            "scripts.setup.tf_apply.terraform_apply_stage1_with_retries",
            side_effect=_fake_stage1,
        ),
        patch(
            "scripts.setup.tf_apply.run_terraform_streaming_with_lock_retry",
            side_effect=_fake_stream,
        ),
        patch("scripts.setup.tf_apply.wait_for_deployed_index_absent") as wait_vvs,
        patch("scripts.setup.tf_apply.ensure_kubectl_context") as ensure_ctx,
        patch("scripts.setup.tf_apply.wait_until_api_ready") as wait_k8s,
        patch("scripts.setup.tf_apply.recover_orphan_gcp_resources", return_value=0),
        patch("scripts.setup.tf_apply.import_persistent_vvs_resources", return_value=0),
        patch("scripts.setup.tf_apply.wait_until_feature_store_names_released"),
        # 2026-05-09 incident hook: tf_apply 冒頭で recover_wif_main を idempotent
        # に呼ぶようになった (WIF 409 再発防止)。test 環境では gcloud 呼出しを mock。
        patch("scripts.setup.tf_apply.recover_wif_main", return_value=0),
    ):
        assert dall._run_tf_apply() == 0

    wait_vvs.assert_called_once_with("mlops-test", "asia-northeast1", "property_embeddings_v3")
    ensure_ctx.assert_called_once_with()
    wait_k8s.assert_called_once_with()
    assert len(stage1_calls) == 1
    assert len(stage2_calls) == 1
    first = stage1_calls[0]
    second = stage2_calls[0]
    assert "terraform" in first[0]
    assert "apply" in first
    assert "-target=module.gke" in first
    assert "-target=module.kserve" not in first
    assert "terraform" in second[0]
    assert "apply" in second
    assert all(not arg.startswith("-target=") for arg in second), second


def test_run_sync_elasticsearch_uses_project_and_default_cluster_url() -> None:
    # 2026-05-10 framework refactor: ECK health wait moved to
    # `DeployStep.precondition`. `_run_sync_elasticsearch` now focuses on the
    # sync body itself; the wait is invoked by the main loop. Therefore this
    # test no longer needs a `wait_until_es_healthy` mock.
    with (
        patch.dict(
            "os.environ",
            {"PROJECT_ID": "mlops-test"},
            clear=False,
        ),
        patch("scripts.setup.deploy_all.sync_elasticsearch_run", return_value=0) as sync_mock,
    ):
        assert dall._run_sync_elasticsearch() == 0

    sync_mock.assert_called_once_with(
        [
            "--project-id=mlops-test",
            "--es-url=http://elasticsearch.search.svc.cluster.local:9200",
        ]
    )


def test_run_sync_elasticsearch_propagates_nonzero_exit() -> None:
    """sync_elasticsearch.run returns shell-style codes; deploy-all must fail the step."""
    with (
        patch.dict("os.environ", {"PROJECT_ID": "mlops-test"}, clear=False),
        patch("scripts.setup.deploy_all.sync_elasticsearch_run", return_value=1),
    ):
        assert dall._run_sync_elasticsearch() == 1


def test_main_invokes_precondition_before_run() -> None:
    """2026-05-10 framework refactor: `DeployStep.precondition` is invoked by
    the main loop immediately before `step.run()`. This test pins the call
    order — precondition first, then run — so the wait cannot be silently
    moved or dropped."""
    call_log: list[str] = []

    def fake_pre() -> None:
        call_log.append("precondition")

    def fake_run() -> int:
        call_log.append("run")
        return 0

    fake_step = dall.DeployStep(
        number=1,
        name="fake",
        label="fake step (with precondition)",
        run=fake_run,
        precondition=fake_pre,
    )

    with (
        patch(
            "scripts.setup.deploy_all._parse_args",
            return_value=argparse.Namespace(from_step="1", to_step="1"),
        ),
        patch("scripts.setup.deploy_all._steps", return_value=[fake_step]),
    ):
        assert dall.main() == 0

    assert call_log == ["precondition", "run"], (
        "main loop must invoke precondition before run "
        "(framework contract for sync-elasticsearch ECK wait)"
    )


def test_main_skips_precondition_when_none() -> None:
    """Steps without a precondition (the default) must not break the main loop."""
    call_log: list[str] = []

    def fake_run() -> int:
        call_log.append("run")
        return 0

    fake_step = dall.DeployStep(
        number=1,
        name="fake",
        label="fake step (no precondition)",
        run=fake_run,
    )

    with (
        patch(
            "scripts.setup.deploy_all._parse_args",
            return_value=argparse.Namespace(from_step="1", to_step="1"),
        ),
        patch("scripts.setup.deploy_all._steps", return_value=[fake_step]),
    ):
        assert dall.main() == 0

    assert call_log == ["run"]


def test_main_propagates_precondition_exception_as_step_failure() -> None:
    """Precondition failures (e.g. ECK 5-min timeout) must surface as a step
    failure with the same logging path as a normal step error."""
    fake_pre_calls = 0

    def fake_pre() -> None:
        nonlocal fake_pre_calls
        fake_pre_calls += 1
        raise TimeoutError("simulated ECK reconcile stall")

    def fake_run() -> int:
        # Should never run because precondition failed.
        raise AssertionError("run() must not be called after precondition failure")

    fake_step = dall.DeployStep(
        number=1,
        name="fake",
        label="fake step",
        run=fake_run,
        precondition=fake_pre,
    )

    with (
        patch(
            "scripts.setup.deploy_all._parse_args",
            return_value=argparse.Namespace(from_step="1", to_step="1"),
        ),
        patch("scripts.setup.deploy_all._steps", return_value=[fake_step]),
        pytest.raises(TimeoutError, match="simulated ECK reconcile stall"),
    ):
        dall.main()
    assert fake_pre_calls == 1
