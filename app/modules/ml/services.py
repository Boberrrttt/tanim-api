import httpx
from fastapi import HTTPException
from typing import Any, Dict, List, Optional

from ...helpers.responses import success_response, error_response

ML_SERVICE_URL = "https://tanim-model.onrender.com"


def _fertilizer_ml_payload(
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph: float,
    crop: str,
    farm_id: Optional[str],
    cycle_start_date: Optional[str],
) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "ph": ph,
        "crop": crop,
    }
    if farm_id is not None:
        body["farm_id"] = farm_id
    if cycle_start_date is not None and str(cycle_start_date).strip() != "":
        body["cycle_start_date"] = str(cycle_start_date).strip()
    return body

async def predict(
    features: List[Any],
    farm_id: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
):
    try:
        async with httpx.AsyncClient() as client:
            payload: dict = {"features": features}
            if farm_id:
                payload["farm_id"] = farm_id
            if lat is not None:
                payload["lat"] = lat
            if lng is not None:
                payload["lng"] = lng

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
    crop: str,
    farm_id: Optional[str] = None,
    cycle_start_date: Optional[str] = None,
):
    try:
        payload = _fertilizer_ml_payload(
            nitrogen,
            phosphorus,
            potassium,
            ph,
            crop,
            farm_id,
            cycle_start_date,
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


def _ml_base() -> str:
    return ML_SERVICE_URL.rstrip("/")


async def proxy_get_pending_soil():
    """Forward GET /pending/soil from tanim-model (global cache on ML instance)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{_ml_base()}/pending/soil",
                timeout=30.0,
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to ML service",
        ) from None
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="ML service timeout",
        ) from None

    if response.status_code == 404:
        try:
            detail = response.json()
        except Exception:
            detail = {
                "status": "waiting",
                "message": "No cached reading on ML service",
            }
        raise HTTPException(status_code=404, detail=detail)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text or "ML pending/soil error",
        )

    return response.json()


async def proxy_delete_pending_soil():
    """Forward DELETE /pending/soil to tanim-model."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{_ml_base()}/pending/soil",
                timeout=30.0,
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to ML service",
        ) from None
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="ML service timeout",
        ) from None

    if response.status_code not in (200, 204):
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text or "ML DELETE pending/soil error",
        )

    if response.content:
        try:
            return response.json()
        except Exception:
            pass
    return {"status": "success", "cleared": True}


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