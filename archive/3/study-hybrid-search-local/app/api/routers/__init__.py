"""HTTP routers for Phase 3 local hybrid search."""

from .feedback_router import router as feedback_router
from .health_router import router as health_router
from .model_router import router as model_router
from .search_router import router as search_router
from .ui_router import build_ui_router

__all__ = [
    "build_ui_router",
    "feedback_router",
    "health_router",
    "model_router",
    "search_router",
]
