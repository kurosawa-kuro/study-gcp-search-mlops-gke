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


def test_es_networkpolicy_allows_eck_operator_namespace() -> None:
    """2026-05-10 incident root cause: `elasticsearch-kibana-policy` NetworkPolicy
    の ingress に `elastic-system` ns が欠落していて、ECK Operator から ES の
    `:9200/_security/api_key` を呼ぶ reconcile が `connect: connection timed out`
    で永続的に block されていた。

    Pin: ECK Operator namespace (`elastic-system`) からの ingress が許可されている。
    削除すると `Phase=ApplyingChanges Health=unknown` reconcile stall が再発する。
    詳細: docs/troubleshooting/eck-license-reconcile-stall.md
    """
    np_yaml = read_text(
        REPO_ROOT / "infra" / "manifests" / "elasticsearch" / "networkpolicy.yaml"
    )
    assert "kubernetes.io/metadata.name: elastic-system" in np_yaml, (
        "elasticsearch-kibana-policy NetworkPolicy must allow ingress from "
        "`elastic-system` namespace (ECK Operator location). Removing this "
        "causes 2026-05-10 reconcile stall to recur."
    )


def test_es_manifest_pins_http_and_anonymous_auth() -> None:
    """2026-05-10 incident: ECK 8.x default は HTTPS + auth 必須だが、本リポの
    canonical URL は `http://elasticsearch.search.svc.cluster.local:9200`
    (Wave 8 contract test で pin 済)。両者の整合のため、ES manifest で:

    1. `spec.http.tls.selfSignedCertificate.disabled: true` (HTTP 化)
    2. `xpack.security.authc.anonymous.username: anonymous_user` + `roles: superuser`
       (anonymous auth bypass、学習プロジェクト前提)

    production 化 (HTTPS + password auth) する時は本 contract を更新すること。
    本 contract は **学習プロジェクト前提を明示する pin** であり、production 化の
    境界判断点でもある (CLAUDE.md「個人技術学習プロジェクト」前提)。
    """
    es_yaml = read_text(
        REPO_ROOT / "infra" / "manifests" / "elasticsearch" / "elasticsearch.yaml"
    )

    # 1. HTTP 化 (TLS 無効)
    assert "selfSignedCertificate:" in es_yaml and "disabled: true" in es_yaml, (
        "ES manifest must set spec.http.tls.selfSignedCertificate.disabled: true "
        "(canonical URL is http://, ECK default HTTPS would cause Server disconnected)"
    )

    # 2. anonymous superuser (auth bypass)
    assert "xpack.security.authc.anonymous.username: anonymous_user" in es_yaml, (
        "ES manifest must define anonymous user for HTTP auth bypass (学習用)"
    )
    assert "xpack.security.authc.anonymous.roles: superuser" in es_yaml, (
        "anonymous user must have superuser role to allow sync-elasticsearch bulk indexing"
    )
