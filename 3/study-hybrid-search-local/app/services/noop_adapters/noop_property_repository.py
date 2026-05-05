from __future__ import annotations

from app.domain.property import Property
from app.services.protocols.property_repository import PropertyRepository


class NoopPropertyRepository(PropertyRepository):
    def fetch(self, property_id: str) -> Property | None:
        return None
