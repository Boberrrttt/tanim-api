from fastapi import HTTPException

from .schemas import FertilizerPredictRequest, PredictionRequest
from .services import (
    get_model_info,
    predict,
    predict_fertilizer,
    proxy_delete_pending_soil,
    proxy_get_pending_soil,
)


async def predict_controller(request: PredictionRequest):
    result = await predict(
        request.features,
        request.farm_id,
        request.lat,
        request.lng,
    )
    if isinstance(result, HTTPException):
        raise result
    return result


async def predict_fertilizer_controller(request: FertilizerPredictRequest):
    result = await predict_fertilizer(
        request.nitrogen,
        request.phosphorus,
        request.potassium,
        request.ph,
        request.crop,
        request.farm_id,
        request.cycle_start_date,
    )
    if isinstance(result, HTTPException):
        raise result
    return result


async def get_model_info_controller():
    result = await get_model_info()
    if isinstance(result, HTTPException):
        raise result
    return result


async def get_pending_soil_controller():
    return await proxy_get_pending_soil()


async def delete_pending_soil_controller():
    return await proxy_delete_pending_soil()

