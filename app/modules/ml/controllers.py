from fastapi import HTTPException

from .schemas import FertilizerPredictRequest, PredictionRequest
from .services import get_model_info, predict, predict_fertilizer


async def predict_controller(request: PredictionRequest):
    result = await predict(request.features, request.farm_id)
    if isinstance(result, HTTPException):
        raise result
    return result


async def predict_fertilizer_controller(request: FertilizerPredictRequest):
    result = await predict_fertilizer(
        request.nitrogen,
        request.phosphorus,
        request.potassium,
        request.ph,
        request.temperature,
        request.ec,
        request.moisture,
        request.farm_id,
    )
    if isinstance(result, HTTPException):
        raise result
    return result


async def get_model_info_controller():
    result = await get_model_info()
    if isinstance(result, HTTPException):
        raise result
    return result

