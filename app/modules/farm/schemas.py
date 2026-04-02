from pydantic import BaseModel
from typing import Optional

class CreateFarm(BaseModel):
    farmer_id: Optional[str] = None
    farm_name: str
    farm_measurement: int
    farm_location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None