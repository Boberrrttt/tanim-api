from fastapi import HTTPException

from .schemas import PredictionRequest
from .services import get_model_info, predict


async def predict_controller(request: PredictionRequest):
    result = await predict(request.features, request.farm_id)
    if isinstance(result, HTTPException):
        raise result
    return result


async def get_model_info_controller():
    result = await get_model_info()
    if isinstance(result, HTTPException):
        raise result
    return result

