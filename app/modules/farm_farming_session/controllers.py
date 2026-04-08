from fastapi import Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from .schemas import StartFarmingSessionBody
from .services import (
    delete_farming_session,
    get_session_by_farm_id,
    list_sessions_by_farmer,
    start_farming_session,
)


async def start_farming_session_controller(
    body: StartFarmingSessionBody,
    db: Session = Depends(get_db),
):
    return await start_farming_session(db, body)


async def get_farming_session_by_farm_controller(
    farm_id: str,
    db: Session = Depends(get_db),
):
    return await get_session_by_farm_id(db, farm_id)


async def list_farming_sessions_by_farmer_controller(
    farmer_id: str,
    db: Session = Depends(get_db),
):
    return await list_sessions_by_farmer(db, farmer_id)


async def delete_farming_session_controller(
    farm_id: str,
    farmer_id: str = Query(..., description="Must match farm.farmer_id"),
    db: Session = Depends(get_db),
):
    return await delete_farming_session(db, farm_id, farmer_id)
