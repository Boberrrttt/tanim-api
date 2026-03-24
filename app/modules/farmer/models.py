from typing import Optional
from datetime import datetime
import uuid

class Farmer:
    def __init__(
        self,
        username: str,
        password: str,
        farmer_id: Optional[str] = None,
        farm_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.farmer_id = farmer_id or str(uuid.uuid4()) 
        self.username = username
        self.password = password
        self.farm_id = farm_id
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "farmer_id": self.farmer_id,
            "username": self.username,
            "password": self.password,
            "farm_id": self.farm_id,
            "created_at": self.created_at.isoformat()
        }

    def to_public_dict(self):
        """Excludes password for API responses."""
        return {
            "farmer_id": str(self.farmer_id),
            "username": self.username,
            "farm_id": self.farm_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

