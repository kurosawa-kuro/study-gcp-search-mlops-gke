"""Shared helpers for Phase 3 workflow contract tests."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def read_repo_file(rel: str) -> str:
    """Read a repository-relative text file as utf-8."""
    return (REPO_ROOT / rel).read_text(encoding="utf-8")
