import httpx
from typing import Any, Dict, List, Optional

from ...helpers.responses import success_response, error_response

ML_SERVICE_URL = "https://tanim-model.onrender.com"


def _fertilizer_ml_payload(
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph: float,
    temperature: float,
    ec: float,
    moisture: float,
    farm_id: Optional[str],
) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "ph": ph,
        "temperature": temperature,
        "ec": ec,
        "moisture": moisture,
    }
    if farm_id is not None:
        body["farm_id"] = farm_id
    return body

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


async def predict_fertilizer(
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph: float,
    temperature: float,
    ec: float,
    moisture: float,
    farm_id: Optional[str] = None,
):
    try:
        payload = _fertilizer_ml_payload(
            nitrogen,
            phosphorus,
            potassium,
            ph,
            temperature,
            ec,
            moisture,
            farm_id,
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ML_SERVICE_URL}/predict/fertilizer",
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
                    message=result.get("message", "Fertilizer inference failed"),
                    details=result if isinstance(result, dict) else None,
                )

            inner = result.get("data", result)
            return success_response(
                message=result.get("message", "Fertilizer prediction successful"),
                data=inner,
            )

    except httpx.TimeoutException:
        return error_response(message="ML service timeout")
    except httpx.ConnectError:
        return error_response(message="Cannot connect to ML service")
    except Exception as e:
        return error_response(message=f"Fertilizer prediction failed: {str(e)}")


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