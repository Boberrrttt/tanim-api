from sqlalchemy.orm import Session
from .services import create, get_by_farm_id
from .schemas import CreateSoilHealthTest
from ...core.database import get_db
from fastapi import Depends

async def create_soil_health_test_controller(soil_health_test: CreateSoilHealthTest, db: Session = Depends(get_db)):
    return await create(db, soil_health_test)

async def get_soil_health_tests_by_farm_id_controller(farm_id: str, db: Session = Depends(get_db)):
    return await get_by_farm_id(db, farm_id)
