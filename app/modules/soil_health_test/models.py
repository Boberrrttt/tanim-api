from typing import Optional
from datetime import datetime
import uuid

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
        classification: str,
        created_at: Optional[datetime] = None
    ):
        self.nitrogen = nitrogen,
        self.phosphorus = phosphorus,
        self.potassium = potassium,
        self.ph = ph,
        self.salinity = salinity,
        self.temperature = temperature,
        self.moisture = moisture,
        self.farm_id = farm_id,
        self.classification = classification,
        self.created_at = created_at or datetime.utcnow()

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
            "classification": self.classification,
            "created_at": self.created_at.isoformat()
        }

