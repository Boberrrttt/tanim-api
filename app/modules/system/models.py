from typing import Optional
from datetime import datetime

class SoilHealthTest:
    def __init__(
        self,
        system_id: str,
        battery_status: float,
        created_at: Optional[datetime] = None
    ):
        self.system_id = system_id
        self.battery_status = battery_status
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "system_id": self.system_id,
            "battery_status": self.battery_status,
            "created_at": self.created_at.isoformat()
        }

