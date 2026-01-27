from pydantic import BaseModel

class CreateSystem(BaseModel):
    battery_status: float

class UpdateBatteryStatus(BaseModel):
    system_id: str
    battery_status: float