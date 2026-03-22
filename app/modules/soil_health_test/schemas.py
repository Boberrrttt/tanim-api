from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
    created_at: Optional[datetime] = None


class UpdateSoilHealthTest(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    salinity: float
    temperature: float
    moisture: float
    farm_id: str
    classification: str
    created_at: Optional[datetime] = None