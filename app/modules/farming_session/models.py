from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
import uuid


@dataclass
class FarmingSession:
    """In-memory shape for a `farming_session` row (DB access is raw SQL in services)."""

    farm_id: str
    farmer_id: str
    selected_crops: str
    soil_snapshot: dict[str, Any]
    fertilizer_recommendation: dict[str, Any]
    farming_session_id: Optional[str] = None
    top_crop_probabilities: Optional[list[dict[str, Any]]] = None
    cycle_start_date: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.farming_session_id = self.farming_session_id or str(uuid.uuid4())

    def to_dict(self) -> dict[str, Any]:
        created = self.created_at
        created_iso = created.isoformat() if created and hasattr(created, "isoformat") else None
        out: dict[str, Any] = {
            "farming_session_id": self.farming_session_id,
            "farm_id": self.farm_id,
            "farmer_id": self.farmer_id,
            "selected_crops": self.selected_crops,
            "soil_snapshot": self.soil_snapshot,
            "fertilizer_recommendation": self.fertilizer_recommendation,
            "top_crop_probabilities": self.top_crop_probabilities,
            "cycle_start_date": self.cycle_start_date,
            "created_at": created_iso,
            # Mobile client fields (tanim-app FarmingSessionRow)
            "started_at": created_iso,
            "selected_crop": self.selected_crops,
        }
        return out
