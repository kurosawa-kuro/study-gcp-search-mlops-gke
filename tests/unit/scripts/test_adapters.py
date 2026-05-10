"""Unit tests for `scripts/adapters/{kubectl,gcloud,terraform}.py`.

Pin the M-Wave8.6 seed 期 contract: thin adapters around CLI tools that
forward args correctly and provide a single mock target per CLI.
"""

from __future__ import annotations

from unittest.mock import patch

from scripts.adapters.gcloud import gcloud_run
from scripts.adapters.kubectl import kubectl_run
from scripts.adapters.terraform import terraform_run


class _FakeProc:
    def __init__(self, stdout: str = "") -> None:
        self.stdout = stdout
        self.returncode = 0


def test_kubectl_run_prefixes_kubectl_to_args() -> None:
    """`kubectl_run("get", "pods")` must invoke `["kubectl", "get", "pods"]`."""
    with patch("scripts.adapters.kubectl._run", return_value=_FakeProc()) as mock:
        kubectl_run("get", "pods", "-n", "search")
    cmd = mock.call_args[0][0]
    assert cmd == ["kubectl", "get", "pods", "-n", "search"]


def test_kubectl_run_forwards_capture_check_timeout() -> None:
    with patch("scripts.adapters.kubectl._run", return_value=_FakeProc("v1.30")) as mock:
        kubectl_run("version", capture=True, check=False, timeout=10)
    kwargs = mock.call_args[1]
    assert kwargs == {"capture": True, "check": False, "timeout": 10}


def test_terraform_run_inserts_chdir_flag() -> None:
    """`terraform_run("output", chdir="/x")` must produce `["terraform", "-chdir=/x", "output"]`."""
    with patch("scripts.adapters.terraform._run", return_value=_FakeProc()) as mock:
        terraform_run("output", "-json", chdir="/path/to/infra")
    cmd = mock.call_args[0][0]
    assert cmd == ["terraform", "-chdir=/path/to/infra", "output", "-json"]


def test_terraform_run_omits_chdir_when_none() -> None:
    """No `chdir` → no `-chdir=` flag (avoid empty `-chdir=` typo)."""
    with patch("scripts.adapters.terraform._run", return_value=_FakeProc()) as mock:
        terraform_run("version")
    cmd = mock.call_args[0][0]
    assert cmd == ["terraform", "version"]


def test_gcloud_run_prefixes_gcloud_to_args() -> None:
    """`gcloud_run("services", "enable", ...)` must invoke `["gcloud", "services", "enable", ...]`.

    2026-05-10 update: signature unified with kubectl_run / terraform_run
    (returns CompletedProcess, not stripped string). Legacy `_common.gcloud`
    remains for back-compat but new callers should use this adapter.
    """
    with patch("scripts.adapters.gcloud._run", return_value=_FakeProc()) as mock:
        gcloud_run("services", "enable", "--project=mlops-dev-a", "iam.googleapis.com")
    cmd = mock.call_args[0][0]
    assert cmd == ["gcloud", "services", "enable", "--project=mlops-dev-a", "iam.googleapis.com"]


def test_gcloud_run_forwards_capture_check_timeout() -> None:
    with patch("scripts.adapters.gcloud._run", return_value=_FakeProc("token...")) as mock:
        gcloud_run("auth", "print-access-token", capture=True, check=False, timeout=10)
    kwargs = mock.call_args[1]
    assert kwargs == {"capture": True, "check": False, "timeout": 10}
