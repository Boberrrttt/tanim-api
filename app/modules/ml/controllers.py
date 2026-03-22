from .services import predict, get_model_info
from .schemas import PredictionRequest

async def predict_controller(request: PredictionRequest):
    return await predict(request.features, request.farm_id)

async def get_model_info_controller():
    return await get_model_info()

