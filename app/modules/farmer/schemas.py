from pydantic import BaseModel 
from typing import Optional
from datetime import datetime

class FarmerCreate(BaseModel):
    username: str
    password: str

class FarmerRead(BaseModel):
    farmer_id: str
    username: str
    farm_id: Optional[str] = None
    created_at: Optional[datetime] = None

