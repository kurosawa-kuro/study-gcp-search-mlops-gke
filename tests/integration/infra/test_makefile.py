from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_makefile_declares_destroy_coast_down_target() -> None:
    """`destroy-coast-down` is the post-Phase rename of the legacy
    `destroy-phase7-learning` placeholder. Keep the target alive (even as a
    placeholder) so docs/runbook/05_運用.md can reference a stable Make target
    name when the coast-down workflow is wired in."""
    text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "destroy-coast-down:" in text
    assert "destroy-phase7-learning:" not in text, (
        "Legacy Phase-prefixed target name leaked back in"
    )
