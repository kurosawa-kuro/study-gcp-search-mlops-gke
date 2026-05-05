"""Phase 3 — Browser UI router (Phase 7 から流用、search-user 1 page のみ).

Phase 7 の `ui_router.py` から ``ui-search-dev`` / ``ui-model-metrics`` /
``ui-data`` / ``ui-ops`` を削除した最小版。

UI ページは AJAX `fetch()` で `/search` / `/feedback` を叩く。
Jinja2 templates は `app/templates/`、static asset は `app/static/`。
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_container
from app.composition_root import Container


def build_ui_router(*, app_root: Path) -> APIRouter:
    router = APIRouter()
    templates = Jinja2Templates(directory=str(app_root / "templates"))

    @router.get("/ui/", name="ui-home")
    @router.get("/ui", name="ui-home-noslash", include_in_schema=False)
    def ui_home(request: Request) -> object:
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "active": "search-user",
                "page_mode": "user",
                "default_query": "新宿区西新宿 1LDK",
                "default_max_rent": 150000,
                "default_top_k": 20,
            },
        )

    @router.get("/ui/property/{property_id}", name="ui-property-detail")
    def ui_property_detail(
        request: Request,
        property_id: str,
        container: Annotated[Container, Depends(get_container)],
        search_id: str | None = None,
    ) -> object:
        property_row = container.property_repository.fetch(property_id)
        if property_row is None:
            raise HTTPException(status_code=404, detail=f"property not found: {property_id}")
        impression = (
            container.event_repository.read_impression(search_id=search_id, property_id=property_id)
            if search_id
            else None
        )
        return templates.TemplateResponse(
            request,
            "property_detail.html",
            {
                "active": "search-user",
                "page_mode": "user",
                "property": property_row,
                "impression": impression,
                "search_id": search_id,
            },
        )

    @router.get("/", include_in_schema=False)
    def root_redirect() -> RedirectResponse:
        return RedirectResponse(url="/ui/", status_code=308)

    return router
