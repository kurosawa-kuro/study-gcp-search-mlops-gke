"""Guard: `Path(__file__).resolve().parents[N] / "<top-level dir>"` must resolve.

When a module is moved to a different directory depth (e.g. the M-Wave8.6
`scripts/` → `scripts/domain/gcp/` reorg), a hard-coded `parents[N]` that used
to land on the repo root now lands one or two levels too shallow. The resulting
`INFRA = .../scripts/infra/terraform/environments/dev` does not exist, so any
`terraform -chdir=<that>` exits non-zero — and because these paths sit on
deploy/ops-only code paths, `make check` never exercises them. They detonate
mid-`deploy-all` instead (observed: `feature_view_sync` step 12 → "terraform
output -json failed", `state_recovery.main()` for `make state-recover`).

This static scan resolves every `Path(__file__).resolve().parents[N] / "<seg>"`
under `scripts/` and asserts the first path segment names a directory that
actually exists relative to that base.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
_PARENTS_PATH_RE = re.compile(
    r"""Path\(__file__\)\.resolve\(\)\.parents\[(\d+)\]\s*/\s*["']([^"']+)["']"""
)


def test_scripts_parents_paths_resolve() -> None:
    offenders: list[str] = []
    for path in (REPO_ROOT / "scripts").rglob("*.py"):
        src = path.read_text(encoding="utf-8")
        for m in _PARENTS_PATH_RE.finditer(src):
            depth = int(m.group(1))
            first_seg = m.group(2)
            base = path.resolve().parents[depth]
            target = base / first_seg
            if not target.exists():
                lineno = src[: m.start()].count("\n") + 1
                offenders.append(
                    f"{path.relative_to(REPO_ROOT)}:{lineno} → parents[{depth}] / "
                    f'"{first_seg}" = {target} (does not exist)'
                )
    assert not offenders, (
        "hard-coded `parents[N]` no longer lands on the intended directory "
        "(module probably moved without bumping N). Offenders:\n  " + "\n  ".join(offenders)
    )
