from datetime import datetime
from typing import Any, Dict, List, Optional


class CropRecommendation:
    def __init__(
        self,
        farm_id: str,
        probabilities: List[Dict[str, Any]],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.farm_id = farm_id
        self.probabilities = probabilities
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at

    def to_dict(self):
        created = self.created_at.isoformat() if hasattr(self.created_at, "isoformat") else self.created_at
        updated = (
            self.updated_at.isoformat()
            if self.updated_at is not None and hasattr(self.updated_at, "isoformat")
            else self.updated_at
        )
        return {
            "farm_id": self.farm_id,
            "probabilities": self.probabilities,
            "created_at": created,
            "updated_at": updated,
        }
