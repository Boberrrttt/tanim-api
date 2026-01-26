from sqlalchemy.orm import Session 
from .services import create, get_all 
from .schemas import CreateFarm 
from ...core.database import get_db 
from fastapi import HTTPException, Depends 
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

async def get_all_farms_controller(db: Session = Depends(get_db)) -> dict:
    try: 
        result = await get_all(db)

        if result["status"] == "error":
            raise HTTPException(
                status_code=401,
                detail={
                    "status": "error",
                    "message": "Farm retrieval failed"
                }
            )

        return success_response(
            message="Farm retrieval successful",
            data=result
        )

    except Exception as e:
        print(e)
        raise error_response(
            message="Farm retrieval failed"
        )