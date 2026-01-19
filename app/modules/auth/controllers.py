from .schemas import Login, LoginRead
from sqlalchemy.orm import Session
from .services import login_farmer, login_admin, signup_farmer
from fastapi import Response, Depends
from ...helpers.responses import error_response, success_response
from ...core.database import get_db

async def login_farmer_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await login_farmer(db, payload)

        response.set_cookie(
            key="refresh_token",
            value=result['refresh_token'],
            httponly=True,  
            secure=True,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )

        return success_response(
            message="Login successful",
            data={
                "farmer_id": result['farmer_id'],
                "username": result['username'],
                "access_token": result['access_token']
            }
        )
    except Exception as e:
        print(e)
        raise error_response(
            message="Login failed"
        )


async def login_admin_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await login_admin(db, payload)

        response.set_cookie(
            key="refresh_token",
            value=result['refresh_token'],
            httponly=True,  
            secure=False,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )

        return success_response(
            message="Login successful",
            data={
                "admin_id": result['admin_id'],
                "username": result['username'],
                "access_token": result['access_token']
            }
        )
    except Exception as e:
        print(e)
        raise error_response(
            message="Login failed"
        )

async def signup_farmer_controller(payload: Login, response: Response, db: Session = Depends(get_db)) -> dict:
    try:
        result = await signup_farmer(db, payload)

        response.set_cookie(
            key="refresh_token",
            value=result['refresh_token'],
            httponly=True,  
            secure=True,    
            samesite="none", 
            max_age=3 * 24 * 60 * 60  
        )
        
        return success_response(
            message="Signup successful",
            data={
                "farmer_id": result['farmer_id'],
                "username": result['username'],
                "access_token": result['access_token']
            }
        )
    except Exception as e:
        print(e)
        raise error_response(
            message="Signup failed"
        )

