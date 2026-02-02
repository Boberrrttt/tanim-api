from .services import predict, get_model_info
from .schemas import PredictionRequest, PredictionResponse, ModelInfoResponse
from fastapi import HTTPException

async def predict_controller(request: PredictionRequest):
    try:
        result = await predict(request.features)
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return PredictionResponse(prediction=result["data"]["prediction"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

async def get_model_info_controller():
    try:
        result = await get_model_info()
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return ModelInfoResponse(**result["data"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")
