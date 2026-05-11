"""Guard: no raw `subprocess.run(..., capture=...)` calls.

`scripts._common.run()` (and the `gcloud_run` / `kubectl_run` / `terraform_run`
adapters) take a `capture=` kwarg, but the **stdlib** `subprocess.run` does not —
it spells the same thing `capture_output=`. Passing `capture=True` straight to
`subprocess.run` raises `TypeError: Popen.__init__() got an unexpected keyword
argument 'capture'` at runtime, and only on code paths `make check` never
exercises (e.g. `state_recovery._recover_dataform`, `vertex_feature_store_wait`)
— so it slips through CI and detonates mid-`deploy-all`.

This static scan pins the contract: any direct `subprocess.run(...)` call that
uses `capture=` must use `capture_output=` (and, for text output, `text=True`).
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCAN_DIRS = ("scripts", "app", "ml", "pipeline", "tools")


def _is_subprocess_run(call: ast.Call) -> bool:
    func = call.func
    # subprocess.run(...)
    if isinstance(func, ast.Attribute) and func.attr == "run":
        val = func.value
        if isinstance(val, ast.Name) and val.id == "subprocess":
            return True
    # bare run(...) is the _common wrapper (different signature) — ignore it
    return False


def _offending_calls(tree: ast.AST) -> list[int]:
    bad: list[int] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _is_subprocess_run(node):
            kwargs = {kw.arg for kw in node.keywords if kw.arg}
            if "capture" in kwargs:  # stdlib subprocess.run has no such kwarg
                bad.append(node.lineno)
    return bad


def test_no_raw_subprocess_run_capture_kwarg() -> None:
    offenders: list[str] = []
    for sub in SCAN_DIRS:
        root = REPO_ROOT / sub
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for lineno in _offending_calls(tree):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{lineno}")
    assert not offenders, (
        "subprocess.run() does not accept `capture=` — use `capture_output=True` "
        "(add `text=True` for str output), or call scripts._common.run(). Offenders:\n  "
        + "\n  ".join(offenders)
    )
