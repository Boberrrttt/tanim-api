from pydantic import BaseModel
from typing import Optional, Dict, Any

class CreateFarm(BaseModel):
    farmer_id: str
    farm_name: str
    farm_measurement: int
    farm_location: Optional[Dict[str, Any]] = None