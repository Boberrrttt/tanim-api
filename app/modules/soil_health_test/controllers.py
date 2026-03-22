from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from .schemas import CreateSoilHealthTest, UpdateSoilHealthTest
from .services import create, get_by_farm_id, update_today


async def create_soil_health_test_controller(soil_health_test: CreateSoilHealthTest, db: Session = Depends(get_db)):
    return await create(db, soil_health_test)


async def update_soil_health_test_controller(payload: UpdateSoilHealthTest, db: Session = Depends(get_db)):
    return await update_today(db, payload)


async def get_soil_health_tests_by_farm_id_controller(farm_id: str, db: Session = Depends(get_db)):
    return await get_by_farm_id(db, farm_id)
