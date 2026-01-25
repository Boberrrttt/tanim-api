from sqlalchemy.orm import Session 
from .services import create 
from .schemas import CreateFarm 
from ...core.database import get_db 
from fastapi import HTTPException, Response, Depends 
from ...helpers.responses import error_response, success_response 

async def create_farm_controller(payload: CreateFarm, db: Session = Depends(get_db),) -> dict:
    try: 
        result = await create(db, payload)

        if result["status"] == "error":
            raise HTTPException(
                status_code=401,
                detail={
                    "status": "error",
                    "message": "Farm creation failed"
                }
            )

        return success_response(
            message="Farm created successfully",
            data=result
        )
    
    except Exception as e:
        print(e)
        raise error_response(
            message="Farm creation failed"
        )