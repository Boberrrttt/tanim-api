from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class Farm:
    def __init__(
        self,
        farm_name: str,
        farm_measurement: int,
        farm_id: Optional[str] = None,
        farm_location: Dict[str, Any] = None,
        created_at: Optional[datetime] = None
    ):
        self.farm_id = farm_id or str(uuid.uuid4()) 
        self.farm_name = farm_name
        self.farm_measurement = farm_measurement
        self.farm_location = farm_location
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "farm_id": self.farm_id,
            "farm_name": self.farm_name,
            "farm_measurement": self.farm_measurement,
            "farm_location": self.farm_location,
            "created_at": self.created_at.isoformat()
        }

