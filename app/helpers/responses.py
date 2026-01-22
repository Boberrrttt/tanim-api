from fastapi import HTTPException, status
from typing import Any, Optional, Dict

def success_response(
    message: str = "Operation successful",
    data: Optional[Any] = None,
    status_code: int = status.HTTP_200_OK
) -> Dict[str, Any]:
    response = {
        "status": "success",
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return response

def error_response(
    message: str = "An error occurred",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: Optional[Dict[str, Any]] = None
) -> HTTPException:
    response: dict = {
        "status": "error",
        "message": message
    }
    
    if details is not None:
        response["details"] = details
    
    return HTTPException(
        status_code=status_code,
        detail=response
    )
