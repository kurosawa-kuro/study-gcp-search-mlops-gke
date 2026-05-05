"""API surface 4-axis prefix contract.

Wave 1 (2026-05-06) で API endpoint を 4 軸 prefix に整理した:

- ``/api/v1/*``  公開 API (バージョン付き、エンドユーザー契約)
- ``/ops/*``     運用 API (operator / developer、IAP-gated)
- ``/ui/*``      Operator UI (Jinja、IAP-gated)
- root reserved: ``/``  ``/livez``  ``/healthz``  ``/readyz``  ``/metrics``
                  ``/static/*``  ``/docs``  ``/redoc``  ``/openapi.json``

このテストは ``app.create_app()`` の routing tree を走査し、上記 4 軸の
**いずれにも属さない path が混入していない** ことを契約として固定する。
旧 ``/search`` / ``/feedback`` / ``/jobs/check-retrain`` / ``/model/*`` は
1 sprint 互換のため ``RedirectResponse(307)`` で残置中。
"""

from __future__ import annotations

import pytest
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

# Allowed prefixes (新 canonical の 4 軸).
_AXIS_PREFIXES: tuple[str, ...] = ("/api/v1/", "/ops/", "/ui/")

# Root-reserved exact paths (probes / Prometheus / FastAPI 標準 / static).
_ROOT_RESERVED_EXACT: frozenset[str] = frozenset(
    {
        "/",
        "/livez",
        "/healthz",
        "/readyz",
        "/metrics",
        "/docs",
        "/docs/oauth2-redirect",
        "/redoc",
        "/openapi.json",
    }
)
_ROOT_RESERVED_PREFIXES: tuple[str, ...] = ("/static/",)

# 1-sprint 互換のために残置している旧 path (Wave 1 終了後に削除予定).
_LEGACY_REDIRECTS: dict[str, str] = {
    "/search": "/api/v1/search",
    "/feedback": "/api/v1/feedback",
    "/jobs/check-retrain": "/ops/jobs/check-retrain",
    "/model/info": "/ops/model/info",
    "/model/metrics": "/ops/model/metrics",
    "/model/data": "/ops/model/data",
}


@pytest.fixture
def app_no_lifespan(monkeypatch: pytest.MonkeyPatch):  # type: ignore[no-untyped-def]
    """Build the real ``app`` but skip the lifespan / ContainerBuilder.

    Mirrors ``tests/unit/app/test_main_routing.py``. Container-backed
    endpoints (``/api/v1/search`` 等) is not exercised here — only the
    routing topology is asserted.
    """
    from app import main
    from app.composition_root import ContainerBuilder

    real_init = ContainerBuilder.__init__

    class _NoopContainer:
        pass

    def _build(self):  # type: ignore[no-untyped-def]
        return _NoopContainer()

    monkeypatch.setattr(
        ContainerBuilder,
        "__init__",
        lambda self, settings, **kwargs: real_init(self, settings, **kwargs),
    )
    monkeypatch.setattr(ContainerBuilder, "build", _build)
    return main.create_app()


def _all_paths(app) -> list[str]:  # type: ignore[no-untyped-def]
    paths: list[str] = []
    for route in app.routes:
        path = getattr(route, "path", None)
        if path is None:
            continue
        paths.append(path)
    return paths


def _classify(path: str) -> str:
    if path in _ROOT_RESERVED_EXACT:
        return "reserved"
    if any(path.startswith(p) for p in _ROOT_RESERVED_PREFIXES):
        return "reserved"
    if any(path.startswith(p) for p in _AXIS_PREFIXES):
        return "axis"
    if path in _LEGACY_REDIRECTS:
        return "legacy"
    return "violation"


def test_all_routes_belong_to_a_known_axis(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """Every route must classify into axis / reserved / legacy.

    Failure means a new endpoint was added without picking a prefix —
    either move it under ``/api/v1/`` or ``/ops/``, or whitelist it in
    the reserved set above with a justification in the docstring.
    """
    violations = [p for p in _all_paths(app_no_lifespan) if _classify(p) == "violation"]
    assert not violations, (
        f"prefix-axis violation: {violations}. "
        "Place new endpoints under /api/v1/ (public) or /ops/ (operator)."
    )


def test_canonical_public_endpoints_exist(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """``/api/v1/search`` / ``/api/v1/feedback`` are wired."""
    paths = set(_all_paths(app_no_lifespan))
    assert "/api/v1/search" in paths
    assert "/api/v1/feedback" in paths


def test_canonical_ops_endpoints_exist(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """Operator surface lives under ``/ops/`` after Wave 1."""
    paths = set(_all_paths(app_no_lifespan))
    expected = {
        "/ops/jobs/check-retrain",
        "/ops/model/info",
        "/ops/model/metrics",
        "/ops/destroy-check",
        "/ops/search-volume",
        "/ops/runs-recent",
    }
    missing = expected - paths
    assert not missing, f"ops surface missing: {missing}"


def test_legacy_paths_redirect_to_new_prefix(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """Old root paths still resolve via 307 (POST-method-preserving)."""
    with TestClient(app_no_lifespan) as client:
        for old_path, new_path in _LEGACY_REDIRECTS.items():
            response = client.request(
                method="POST" if old_path in {"/search", "/feedback", "/jobs/check-retrain"} else "GET",
                url=old_path,
                follow_redirects=False,
            )
            assert response.status_code == 307, (
                f"{old_path}: expected 307, got {response.status_code}"
            )
            assert response.headers["location"] == new_path, (
                f"{old_path}: expected redirect to {new_path}, got {response.headers['location']}"
            )


def test_probes_are_not_namespaced(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """``/livez`` / ``/healthz`` / ``/readyz`` MUST stay at root for k8s.

    k8s probes are wired via ``startupProbe`` / ``livenessProbe`` /
    ``readinessProbe`` paths in ``infra/manifests/search-api/deployment.yaml``;
    moving them under a prefix would break the cluster contract silently.
    """
    paths = set(_all_paths(app_no_lifespan))
    for required in ("/livez", "/healthz", "/readyz"):
        assert required in paths, f"probe {required} missing"


def test_metrics_endpoint_at_root(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """``/metrics`` MUST stay at root for GMP / Prometheus scrape."""
    paths = set(_all_paths(app_no_lifespan))
    assert "/metrics" in paths


def test_legacy_redirects_excluded_from_openapi_schema(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """Legacy 307 routes must NOT appear in OpenAPI schema (deprecated path noise)."""
    schema_paths = set(app_no_lifespan.openapi().get("paths", {}).keys())
    leaked = schema_paths & set(_LEGACY_REDIRECTS.keys())
    assert not leaked, f"legacy redirect leaked into OpenAPI: {leaked}"


def test_canonical_paths_appear_in_openapi_schema(app_no_lifespan) -> None:  # type: ignore[no-untyped-def]
    """New ``/api/v1/*`` and ``/ops/*`` are documented in the OpenAPI."""
    schema_paths = set(app_no_lifespan.openapi().get("paths", {}).keys())
    must_appear = {
        "/api/v1/search",
        "/api/v1/feedback",
        "/ops/jobs/check-retrain",
        "/ops/model/info",
        "/ops/model/metrics",
    }
    missing = must_appear - schema_paths
    assert not missing, f"OpenAPI missing canonical paths: {missing}"


def test_route_iap_policy_documents_prefix_axes() -> None:
    """IAP policy YAML must document the 4-axis prefix structure.

    The actual per-prefix matchers belong to a future HTTPRoute split, but
    the rationale must be pinned in YAML comments so the next reviewer
    knows the intent.
    """
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[3]
    policy = (
        repo_root / "infra" / "manifests" / "policies" / "search-api-iap-policy.yaml"
    ).read_text(encoding="utf-8")
    for required_marker in (
        "/api/v1/",
        "/ops/",
        "/ui/",
        "/livez /healthz /readyz",
    ):
        assert required_marker in policy, (
            f"IAP policy lost prefix-axis comment: {required_marker!r}"
        )
