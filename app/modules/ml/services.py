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
                timeout=120.0,
            )

            if response.status_code != 200:
                return error_response(
                    message=f"ML service error: {response.status_code}",
                    details={"response": response.text},
                )

            result = response.json()
            if result.get("status") == "error":
                return error_response(
                    message=result.get("message", "ML inference failed"),
                    details=result if isinstance(result, dict) else None,
                )

            inner = result.get("data", result)
            return success_response(
                message="Prediction successful",
                data=inner,
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
                timeout=30.0,
            )

            if response.status_code != 200:
                return error_response(
                    message=f"ML service error: {response.status_code}",
                    details={"response": response.text},
                )

            result = response.json()
            inner = result.get("data", result)
            return success_response(
                message="Model info retrieved",
                data=inner,
            )
                
    except httpx.TimeoutException:
        return error_response(message="ML service timeout")
    except httpx.ConnectError:
        return error_response(message="Cannot connect to ML service")
    except Exception as e:
        return error_response(message=f"Failed to get model info: {str(e)}")