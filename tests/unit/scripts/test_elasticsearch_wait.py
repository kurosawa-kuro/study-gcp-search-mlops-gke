"""Unit tests for scripts.domain.k8s.elasticsearch_wait.

Pin the 2026-05-09 incident fix: deploy-all step 10 (sync-elasticsearch) must
not start until ECK Elasticsearch CR `.status.health` is green or yellow.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from scripts.domain.k8s import elasticsearch_wait
from scripts.domain.k8s.elasticsearch_wait import (
    HEALTHY_STATES,
    wait_until_es_healthy,
)


class _FakeProc:
    def __init__(self, stdout: str) -> None:
        self.stdout = stdout
        self.stderr = ""
        self.returncode = 0


def test_wait_returns_immediately_on_green() -> None:
    """If ES is already green on the first poll, return without sleeping."""
    with (
        patch(
            "scripts.domain.k8s.elasticsearch_wait.subprocess.run",
            return_value=_FakeProc("green"),
        ),
        patch("scripts.domain.k8s.elasticsearch_wait.time.sleep") as sleep_mock,
    ):
        assert wait_until_es_healthy(timeout_s=60) == "green"
    # No sleep on the happy path — first poll succeeds.
    sleep_mock.assert_not_called()


def test_wait_accepts_yellow_for_single_node_cluster() -> None:
    """Single-node ECK CR is always yellow at best (replicas unallocatable);
    sync-elasticsearch must accept yellow."""
    with (
        patch(
            "scripts.domain.k8s.elasticsearch_wait.subprocess.run",
            return_value=_FakeProc("yellow"),
        ),
        patch("scripts.domain.k8s.elasticsearch_wait.time.sleep"),
    ):
        assert wait_until_es_healthy(timeout_s=60) == "yellow"


def test_wait_polls_until_health_becomes_green() -> None:
    """Walk health through unset → unknown → green and confirm we exit on green."""
    health_values = iter(["", "unknown", "unknown", "green"])
    phase_values = iter(["", "ApplyingChanges", "ApplyingChanges", "Ready"])

    def fake_run(cmd, **kwargs):
        # Distinguish health vs phase calls by jsonpath.
        if "{.status.health}" in cmd[-1]:
            return _FakeProc(next(health_values))
        return _FakeProc(next(phase_values))

    with (
        patch("scripts.domain.k8s.elasticsearch_wait.subprocess.run", side_effect=fake_run),
        patch("scripts.domain.k8s.elasticsearch_wait.time.sleep"),
        # Pretend monotonic always advances by 1s — never hit deadline.
        patch("scripts.domain.k8s.elasticsearch_wait.time.monotonic", side_effect=range(0, 100)),
    ):
        assert wait_until_es_healthy(timeout_s=60) == "green"


def test_wait_raises_timeout_on_stuck_unknown() -> None:
    """ECK reconcile stall (2026-05-09 incident): health stays `unknown`.

    Verify we raise TimeoutError pointing at the troubleshooting doc rather
    than hanging forever. This is the signal to operator that destroy-all is
    the cheaper path (see eck-license-reconcile-stall.md)."""
    with (
        patch(
            "scripts.domain.k8s.elasticsearch_wait.subprocess.run",
            return_value=_FakeProc("unknown"),
        ),
        patch("scripts.domain.k8s.elasticsearch_wait.time.sleep"),
        # monotonic returns 0, then 1000 (past 60s deadline).
        patch("scripts.domain.k8s.elasticsearch_wait.time.monotonic", side_effect=[0, 1000, 1001]),
        pytest.raises(TimeoutError, match="eck-license-reconcile-stall"),
    ):
        wait_until_es_healthy(timeout_s=60)


def test_healthy_states_pin_green_and_yellow() -> None:
    """Pin the contract: only `green` and `yellow` are accepted as healthy."""
    assert elasticsearch_wait.HEALTHY_STATES == ("green", "yellow")
    assert "red" not in HEALTHY_STATES
    assert "unknown" not in HEALTHY_STATES
