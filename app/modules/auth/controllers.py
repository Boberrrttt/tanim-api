from .schemas import Login 
from sqlalchemy.orm import Session
from .services import login_farmer, login_admin, signup_admin, signup_farmer
from fastapi import HTTPException, Response, Depends
from ...helpers.responses import error_response, success_response
from ...core.database import get_db

async def login_farmer_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await login_farmer(db, payload)

        if result["status"] == "error":
            raise HTTPException(
                status_code=401,
                detail={
                    "status": "error",
                    "message": "Invalid username or password"
                }
            )

        response.set_cookie(
            key="refresh_token",
            value=result['data']['refresh_token'],
            httponly=True,  
            secure=True,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )

        response_data = result['data'].copy()
        response_data.pop("refresh_token", None)

        return success_response(
            message="Login successful",
            data=response_data
        )


    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise error_response(
            message="Login failed"
        )


async def login_admin_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await login_admin(db, payload)

        if result["status"] == "error":
            raise HTTPException(
                status_code=401,
                detail={
                    "status": "error",
                    "message": "Invalid username or password"
                }
            )

        response.set_cookie(
            key="refresh_token",
            value=result['data']['refresh_token'],
            httponly=True,  
            secure=False,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )

        response_data = result['data'].copy()
        response_data.pop("refresh_token", None)

        return success_response(
            message="Login successful",
            data=response_data
        )


    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise error_response(
            message="Login failed"
        )


async def signup_farmer_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await signup_farmer(db, payload)

        if result["status"] == "error":
            if result["error"] == "USERNAME_EXISTS":
                raise HTTPException(
                    status_code=409,
                    detail={
                        "status": "error",
                        "message": "Username already exists"
                    }
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "status": "error",
                        "message": "Signup failed"
                    }
                )

        response.set_cookie(
            key="refresh_token",
            value=result['data']['refresh_token'],
            httponly=True,  
            secure=True,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )
        
        response_data = result['data'].copy()
        response_data.pop("refresh_token", None)

        return success_response(
            message="Login successful",
            data=response_data
        )


    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise error_response(
            message="Signup failed"
        )


async def signup_admin_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await signup_admin(db, payload)

        if result["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "error",
                    "message": "Signup failed"
                }
            )

        response.set_cookie(
            key="refresh_token",
            value=result['data']['refresh_token'],
            httponly=True,  
            secure=True,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )
        
        response_data = result['data'].copy()
        response_data.pop("refresh_token", None)

        return success_response(
            message="Login successful",
            data=response_data
        )


    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise error_response(
            message="Signup failed"
        )

