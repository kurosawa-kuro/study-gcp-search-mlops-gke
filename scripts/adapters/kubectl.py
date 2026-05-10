"""Thin adapter around the `kubectl` CLI.

Goal: centralize subprocess invocations to make mocking trivial in tests.
Callers should use `kubectl_run(...)` instead of building `subprocess.run(["kubectl", ...])`
inline. This is one of the 3 adapter modules introduced 2026-05-10 (M-Wave8.6 Phase 3,
sibling: `scripts/adapters/gcloud.py`, `scripts/adapters/terraform.py`).

Why a wrapper instead of direct `subprocess.run`:
- Single mock target per CLI (`scripts.adapters.kubectl.kubectl_run`) avoids the
  2026-05-10 incident pattern where mocking subprocess at multiple call sites was
  error-prone (mock 漏れ → real kubectl 5min hang).
- Future cross-cutting concerns (timeouts, retry, structured logging) can be added
  here without touching ~30 callers.
"""

from __future__ import annotations

import subprocess

from scripts._common import run as _run


def kubectl_run(
    *args: str,
    capture: bool = False,
    check: bool = True,
    timeout: int | None = None,
    input: str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Invoke `kubectl <args...>`. Returns the completed subprocess.

    - ``input`` is fed to ``kubectl``'s stdin (used by ``kubectl apply -f -``).
    - ``env`` overrides the subprocess environment (e.g. ``KUBECONFIG=...``).

    Examples:
        kubectl_run("get", "pods", "-n", "search")
        kubectl_run("apply", "-f", "manifests.yaml", capture=False)
        kubectl_run("apply", "-f", "-", input=manifest_yaml)
        out = kubectl_run("get", "elasticsearch", "-o", "jsonpath={.status.health}", capture=True)
    """
    return _run(
        ["kubectl", *args],
        capture=capture,
        check=check,
        timeout=timeout,
        input=input,
        env=env,
    )
