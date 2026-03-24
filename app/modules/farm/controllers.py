from sqlalchemy.orm import Session 
from .services import create, get_all, get_by_farmer_id
from .schemas import CreateFarm 
from ...core.database import get_db 
from fastapi import Depends 

async def create_farm_controller(payload: CreateFarm, db: Session = Depends(get_db)):
    return await create(db, payload)

async def get_all_farms_controller(db: Session = Depends(get_db)):
    return await get_all(db)

async def get_farms_by_farmer_id_controller(farmer_id: str, db: Session = Depends(get_db)):
    return await get_by_farmer_id(db, farmer_id)