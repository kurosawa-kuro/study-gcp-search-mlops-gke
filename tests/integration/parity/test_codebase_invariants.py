"""Canonical codebase invariants (offline).

Mirrors ``docs/runbook/04_検証.md`` §2 **L1''** (legacy residue) and the
**Elasticsearch-only lexical** policy for **source trees** — not ``docs/``
(runbook itself documents forbidden tokens and would self-match).

These tests exist so **仕様とコードの乖離** is caught in CI without relying on
manual ``rg`` before every PR.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.integration.parity.parity_invariant import REPO_ROOT, read_text

# Same token union as runbook §2 L1'' table (W2-8 removal targets).
W28_LEGACY_SUBSTRINGS: tuple[str, ...] = (
    "BigQuerySemanticSearch",
    "BigQueryFeatureFetcher",
    "SEMANTIC_BACKEND",
    "FEATURE_FETCHER_BACKEND",
    "VERTEX_FEATURE_GROUP_ID",
    "ui_model_metrics_legacy",
    "ui_data_legacy",
    "enable_vertex_endpoint_shell",
    "vertex_encoder_endpoint_id",
    "vertex_reranker_endpoint_id",
)

LEXICAL_LEGACY_SUBSTRINGS: tuple[str, ...] = (
    "MeilisearchLexical",
    "scripts.ops.sync_meili",
    "sync_meili",
    "MEILI_BASE_URL",
    "meili_base_url",
)

_SKIP_DIR_NAMES = frozenset({".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"})


def _walk_files(root: Path, *, suffixes: tuple[str, ...]) -> list[Path]:
    out: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in _SKIP_DIR_NAMES for part in path.parts):
            continue
        if suffixes and path.suffix not in suffixes:
            continue
        out.append(path)
    return sorted(out)


def _find_substring_hits(paths: list[Path], needles: tuple[str, ...]) -> list[tuple[Path, str]]:
    hits: list[tuple[Path, str]] = []
    for path in paths:
        text = read_text(path)
        for needle in needles:
            if needle in text:
                hits.append((path, needle))
    return hits


@pytest.mark.parametrize(
    "root_name",
    ["app", "ml", "pipeline", "scripts"],
)
def test_w2_8_legacy_tokens_absent_in_python_trees(root_name: str) -> None:
    root = REPO_ROOT / root_name
    paths = _walk_files(root, suffixes=(".py",))
    hits = _find_substring_hits(paths, W28_LEGACY_SUBSTRINGS)
    assert not hits, (
        "W2-8 legacy residue reintroduced (see docs/runbook/04_検証.md §2 L1''): "
        f"{[(str(p.relative_to(REPO_ROOT)), n) for p, n in hits]}"
    )


def test_w2_8_legacy_tokens_absent_in_manifests_yaml() -> None:
    root = REPO_ROOT / "infra" / "manifests"
    paths = _walk_files(root, suffixes=(".yaml", ".yml"))
    hits = _find_substring_hits(paths, W28_LEGACY_SUBSTRINGS)
    assert not hits, (
        "W2-8 legacy strings must not appear in committed manifests: "
        f"{[(str(p.relative_to(REPO_ROOT)), n) for p, n in hits]}"
    )


def test_lexical_es_canonical_no_meilisearch_in_app() -> None:
    """``scripts/`` may still name Terraform/GCP cleanup resources (meili-*); app must not."""
    paths = _walk_files(REPO_ROOT / "app", suffixes=(".py",))
    hits = _find_substring_hits(paths, LEXICAL_LEGACY_SUBSTRINGS)
    assert not hits, (
        "Elasticsearch-only lexical path violated (Meilisearch remnants in app): "
        f"{[(str(p.relative_to(REPO_ROOT)), n) for p, n in hits]}"
    )


def test_makefile_has_no_removed_sync_meili_target() -> None:
    makefile = read_text(REPO_ROOT / "Makefile")
    assert "sync-meili:" not in makefile, (
        "Removed legacy target sync-meili — use sync-elasticsearch (runbook / TASKS_ROADMAP)."
    )


def test_pyproject_has_no_sync_meili_console_script() -> None:
    pyproject = read_text(REPO_ROOT / "pyproject.toml")
    assert "sync_meili" not in pyproject, (
        "Remove legacy meili-sync console_script from pyproject.toml"
    )


def test_search_api_deployment_has_no_meili_env_refs() -> None:
    dep = read_text(REPO_ROOT / "infra" / "manifests" / "search-api" / "deployment.yaml")
    assert "MEILI_" not in dep, "deployment.yaml must not reference Meilisearch env vars"
    assert "meili" not in dep.lower(), "deployment.yaml must not reference meili resources"
