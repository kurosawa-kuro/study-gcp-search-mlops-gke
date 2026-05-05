"""FastAPI hybrid-search API — GKE Pod entrypoint.

This module is the **HTTP server entrypoint only**. DI wiring lives in
``app/composition_root.py``; endpoint logic lives in
``app/api/routers/``; mapping in ``app/api/mappers/``; business logic in
``app/services/``.

Route surfaces (kept disjoint by **prefix-axis**):

- **Public API** — ``/api/v1/search`` ``/api/v1/feedback``
  (versioned end-user contract, IAP or future API key gated)
- **Operations API** — ``/ops/jobs/check-retrain`` ``/ops/model/info``
  ``/ops/model/metrics`` ``/ops/destroy-check`` ``/ops/search-volume``
  ``/ops/runs-recent`` (operator-facing, IAP-gated, unversioned)
- **Probes** — ``/livez`` ``/healthz`` ``/readyz`` (k8s, no auth)
- **Prom exposition** — ``/metrics`` (GMP / SLO scrape target, no auth)
- **Browser UI** — ``/ui/`` ``/ui/dev`` ``/ui/dev/model/metrics`` ``/ui/dev/data``
  (``/`` redirects to ``/ui/`` so existing bookmarks still resolve)

Legacy paths (``/search`` ``/feedback`` ``/jobs/check-retrain`` ``/model/*``)
are still mapped via ``RedirectResponse(307)`` for one sprint of
client-migration buffer; remove after the new prefix is canonical.

The Pod keeps only retrieval / orchestration concerns. Query embeddings
and rerank scoring are delegated to KServe InferenceService (cluster-local
HTTP) when configured. PMLE technology integrations (BQML popularity) are
wired in as optional adapters — see ``ContainerBuilder``.

Observability (logging / metrics / future tracing) is bundled in
``app.observability.Observability`` and shared between this entrypoint and
the Container.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.middleware import RequestLoggingMiddleware
from app.api.routers import (
    build_ui_router,
    feedback_router,
    health_router,
    model_router,
    ops_router,
    retrain_router,
    search_router,
)
from app.composition_root import ContainerBuilder
from app.observability import Observability
from app.settings import ApiSettings
from ml.common.logging import configure_logging

# 旧 path → 新 prefix の互換 mapping。1 sprint だけ ``RedirectResponse(307)`` で
# 残す。POST 経路は 308 が一部クライアントで非互換のため 307 (Temporary Redirect、
# method 維持) で固定。
_LEGACY_REDIRECTS: dict[str, str] = {
    "/search": "/api/v1/search",
    "/feedback": "/api/v1/feedback",
    "/jobs/check-retrain": "/ops/jobs/check-retrain",
    "/model/info": "/ops/model/info",
    "/model/metrics": "/ops/model/metrics",
    "/model/data": "/ops/model/data",
}


def _build_legacy_redirects() -> APIRouter:
    """Wire 1-sprint compatibility 307 redirects from old root paths."""
    legacy = APIRouter()
    for old_path, new_path in _LEGACY_REDIRECTS.items():
        target = new_path

        async def _redirect(request: Request, target: str = target) -> RedirectResponse:
            query = request.url.query
            location = f"{target}?{query}" if query else target
            return RedirectResponse(url=location, status_code=307)

        for method in ("GET", "POST"):
            legacy.add_api_route(
                old_path,
                _redirect,
                methods=[method],
                include_in_schema=False,
                deprecated=True,
                name=f"legacy-{old_path}-{method.lower()}",
            )
    return legacy


def create_app() -> FastAPI:
    configure_logging()
    settings = ApiSettings()
    observability = Observability.from_env()
    logger = observability.get_logger("app")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Build the immutable :class:`Container` once and stash on app state."""
        configure_logging(level=os.getenv("LOG_LEVEL", "INFO"))
        app.state.container = ContainerBuilder(settings, observability=observability).build()
        yield

    app = FastAPI(title="gke+kserve-backed hybrid search API", lifespan=lifespan)

    app_root = Path(__file__).resolve().parent
    app.mount("/static", StaticFiles(directory=str(app_root / "static")), name="static")
    app.add_middleware(RequestLoggingMiddleware, logger=logger)

    # /api/v1/* — versioned end-user contract.
    api_v1 = APIRouter(prefix="/api/v1")
    api_v1.include_router(search_router)
    api_v1.include_router(feedback_router)
    app.include_router(api_v1)

    # /ops/* — operator / developer surface (IAP-gated, unversioned).
    # Existing ops_router defines ``/destroy-check`` ``/search-volume``
    # ``/runs-recent`` (no self-prefix); model_router keeps its ``/model``
    # sub-prefix so paths nest cleanly to ``/ops/model/...``.
    ops = APIRouter(prefix="/ops")
    ops.include_router(retrain_router)  # /ops/jobs/check-retrain
    ops.include_router(model_router)  # /ops/model/info, /ops/model/metrics, /ops/model/data
    ops.include_router(ops_router)  # /ops/destroy-check, /ops/search-volume, /ops/runs-recent
    app.include_router(ops)

    # Probes (no prefix, no auth, OpenAPI-excluded by route definitions).
    app.include_router(health_router)

    # 1-sprint legacy 307 redirects from old root paths.
    app.include_router(_build_legacy_redirects())

    # Operator UI is namespaced under /ui/ so /metrics belongs to Prometheus.
    app.include_router(build_ui_router(app_root=app_root), prefix="/ui")

    @app.get("/", include_in_schema=False)
    def _root_redirect() -> RedirectResponse:
        return RedirectResponse(url="/ui/", status_code=308)

    # Prometheus exposition at /metrics. The ``service`` label this emits
    # has to match the SLO module's good/total filter
    # (``metric.label."service"="search-api"`` and ``status=~"2.."``);
    # ``Observability.expose_prometheus`` owns that contract.
    observability.expose_prometheus(app)

    return app


app = create_app()
