from typing import Optional
from datetime import datetime

class SoilHealthTest:
    def __init__(
        self,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        ph: float,
        salinity: float,
        temperature: float,
        moisture: float,
        farm_id: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.nitrogen = nitrogen,
        self.phosphorus = phosphorus,
        self.potassium = potassium,
        self.ph = ph,
        self.salinity = salinity,
        self.temperature = temperature,
        self.moisture = moisture,
        self.farm_id = farm_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "nitrogen": self.nitrogen,
            "phosphorus": self.phosphorus,
            "potassium": self.potassium,
            "ph": self.ph,
            "salinity": self.salinity,
            "temperature": self.temperature,
            "moisture": self.moisture,
            "farm_id": self.farm_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

