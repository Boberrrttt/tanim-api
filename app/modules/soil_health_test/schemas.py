from pydantic import BaseModel
from typing import Optional, Dict, Any

class CreateSoilHealthTest(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    salinity: float 
    temperature: float
    moisture: float
    farm_id: str
    classification: str