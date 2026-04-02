from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FarmerCreate(BaseModel):
    username: str
    password: str
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    phone_number: str = ""

class FarmerRead(BaseModel):
    farmer_id: str
    username: str
    first_name: str
    last_name: str
    phone_number: str = ""
    farm_id: Optional[str] = None
    created_at: Optional[datetime] = None

