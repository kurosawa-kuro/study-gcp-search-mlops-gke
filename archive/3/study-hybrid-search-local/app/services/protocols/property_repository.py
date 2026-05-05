from __future__ import annotations

from typing import Protocol

from app.domain.property import Property


class PropertyRepository(Protocol):
    def fetch(self, property_id: str) -> Property | None: ...
