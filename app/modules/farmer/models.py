from typing import Optional
from datetime import datetime
import uuid

class Farmer:
    def __init__(
        self,
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        phone_number: str = "",
        farmer_id: Optional[str] = None,
        farm_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.farmer_id = farmer_id or str(uuid.uuid4()) 
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.farm_id = farm_id
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "farmer_id": self.farmer_id,
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "farm_id": self.farm_id,
            "created_at": self.created_at.isoformat()
        }

    def to_public_dict(self):
        """Excludes password for API responses."""
        return {
            "farmer_id": str(self.farmer_id),
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "farm_id": self.farm_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

