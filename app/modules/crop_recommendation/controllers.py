from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from .schemas import CreateCropRecommendation, UpdateCropRecommendation
from .services import create, get_by_farm_id, update_today


async def create_crop_recommendation_controller(
    body: CreateCropRecommendation, db: Session = Depends(get_db)
):
    return await create(db, body)


async def update_crop_recommendation_controller(
    payload: UpdateCropRecommendation, db: Session = Depends(get_db)
):
    return await update_today(db, payload)


async def get_crop_recommendations_by_farm_id_controller(
    farm_id: str, db: Session = Depends(get_db)
):
    return await get_by_farm_id(db, farm_id)
