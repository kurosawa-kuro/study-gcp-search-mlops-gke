from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Property:
    property_id: str
    title: str
    description: str
    city: str
    ward: str | None
    layout: str
    rent: int
    walk_min: int
    age_years: int
    area_m2: float
    pet_ok: bool
    created_at: datetime | None = None
