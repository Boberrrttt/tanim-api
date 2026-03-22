import httpx
from typing import Any, List, Optional
from ...helpers.responses import success_response, error_response

ML_SERVICE_URL = "https://tanim-model.onrender.com"

async def predict(features: List[Any], farm_id: Optional[str] = None):
    try:
        async with httpx.AsyncClient() as client:
            payload: dict = {"features": features}
            if farm_id:
                payload["farm_id"] = farm_id

            response = await client.post(
                f"{ML_SERVICE_URL}/predict",
                json=payload,
            )
            
            if response.status_code == 200:
                result = response.json()
                return success_response(
                    message="Prediction successful",
                    data=result.get("data", result)
                )
            else:
                return error_response(
                    message=f"ML service error: {response.status_code}",
                    details={"response": response.text}
                )
                
    except httpx.TimeoutException:
        return error_response(message="ML service timeout")
    except httpx.ConnectError:
        return error_response(message="Cannot connect to ML service")
    except Exception as e:
        return error_response(message=f"Prediction failed: {str(e)}")

async def get_model_info():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ML_SERVICE_URL}/",
            )
            
            if response.status_code == 200:
                result = response.json()
                return success_response(
                    message="Model info retrieved",
                    data=result.get("data", result)
                )
            else:
                return error_response(
                    message=f"ML service error: {response.status_code}",
                    details={"response": response.text}
                )
                
    except httpx.TimeoutException:
        return error_response(message="ML service timeout")
    except httpx.ConnectError:
        return error_response(message="Cannot connect to ML service")
    except Exception as e:
        return error_response(message=f"Failed to get model info: {str(e)}")