"""Unit tests for scripts.infra.terraform_lock."""

from __future__ import annotations

from scripts.infra.terraform_lock import (
    is_state_lock_error,
    parse_terraform_lock_id,
    should_auto_force_unlock,
)


def test_parse_lock_id_from_terraform_stderr() -> None:
    blob = """
[31m│[0m Error acquiring the state lock
Lock Info:
  ID:        1777812961721387
  Who:       ubuntu@host
"""
    assert parse_terraform_lock_id(blob) == "1777812961721387"


def test_is_state_lock_error() -> None:
    assert is_state_lock_error("Error acquiring the state lock") is True
    assert is_state_lock_error("random plan output") is False


def test_should_auto_force_unlock_aliases(monkeypatch) -> None:
    for name in (
        "TERRAFORM_STATE_FORCE_UNLOCK",
        "DESTROY_ALL_FORCE_UNLOCK",
        "DEPLOY_ALL_FORCE_UNLOCK",
    ):
        monkeypatch.delenv("TERRAFORM_STATE_FORCE_UNLOCK", raising=False)
        monkeypatch.delenv("DESTROY_ALL_FORCE_UNLOCK", raising=False)
        monkeypatch.delenv("DEPLOY_ALL_FORCE_UNLOCK", raising=False)
        monkeypatch.setenv(name, "1")
        assert should_auto_force_unlock() is True
    monkeypatch.delenv("TERRAFORM_STATE_FORCE_UNLOCK", raising=False)
    monkeypatch.delenv("DESTROY_ALL_FORCE_UNLOCK", raising=False)
    monkeypatch.delenv("DEPLOY_ALL_FORCE_UNLOCK", raising=False)
    assert should_auto_force_unlock() is False


def test_parse_lock_id_handles_real_ansi_color_output() -> None:
    """2026-05-10 incident: parser failed on real terraform CLI output.

    terraform wraps lock info rows in box-drawing ``│`` + ANSI color escape
    sequences, so the line containing the lock ID actually looks like:

        \\x1b[31m│\\x1b[0m \\x1b[0m  ID:        1778332028753123

    The original ``^\\s*ID:`` anchor fails because the line starts with an
    ANSI escape sequence, not whitespace. The previous test only used a
    space-prefixed ID line and silently masked the bug — it passed even on
    the broken regex. This test pins the real-output behavior.
    """
    real_output = (
        "\x1b[31m╷\x1b[0m\x1b[0m\n"
        "\x1b[31m│\x1b[0m \x1b[1m\x1b[31mError: \x1b[0m\x1b[0m\x1b[1m"
        "Error acquiring the state lock\x1b[0m\n"
        "\x1b[31m│\x1b[0m \x1b[0m\n"
        "\x1b[31m│\x1b[0m \x1b[0mLock Info:\n"
        "\x1b[31m│\x1b[0m \x1b[0m  ID:        1778332028753123\n"
        "\x1b[31m│\x1b[0m \x1b[0m  Path:      gs://example/default.tflock\n"
        "\x1b[31m│\x1b[0m \x1b[0m  Operation: OperationTypeApply\n"
        "\x1b[31m│\x1b[0m \x1b[0m  Who:       ubuntu@host\n"
        "\x1b[31m╵\x1b[0m\x1b[0m\n"
    )
    assert parse_terraform_lock_id(real_output) == "1778332028753123"


def test_parse_lock_id_returns_none_when_absent() -> None:
    assert parse_terraform_lock_id("totally unrelated terraform output") is None
