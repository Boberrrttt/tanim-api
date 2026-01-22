from typing import Optional
from datetime import datetime
import uuid

class Admin:
    def __init__(
        self,
        username: str,
        password: str,
        admin_id: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.admin_id = admin_id or str(uuid.uuid4()) 
        self.username = username
        self.password = password
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "username": self.username,  
            "password": self.password,
            "created_at": self.created_at.isoformat()
        }

