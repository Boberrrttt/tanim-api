from .schemas import CreateSystem, UpdateBatteryStatus
from .services import create, update
from ...core.database import get_db
from fastapi import Depends

async def create_system_controller(payload: CreateSystem, db = Depends(get_db)):
    return await create(db, payload)

async def update_battery_status_controller(payload: UpdateBatteryStatus, db = Depends(get_db)):
    return await update(db, payload)