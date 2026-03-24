from .schemas import Login, SignupFarmer
from sqlalchemy.orm import Session
from .services import login_farmer, login_admin, signup_admin, signup_farmer
from fastapi import Response, Depends
from ...core.database import get_db

async def login_farmer_controller(payload: Login, response: Response, db: Session = Depends(get_db)):
    result = await login_farmer(db, payload)
    
    if hasattr(result, 'detail'):
        raise result
    
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
    
    return result

async def login_admin_controller(payload: Login, response: Response, db: Session = Depends(get_db)):
    result = await login_admin(db, payload)
    
    if hasattr(result, 'detail'):
        raise result
    
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
    
    return result

async def signup_farmer_controller(payload: SignupFarmer, response: Response, db: Session = Depends(get_db)):
    result = await signup_farmer(db, payload)
    
    if hasattr(result, 'detail'):
        raise result

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
    
    return result

async def signup_admin_controller(payload: Login, response: Response, db: Session = Depends(get_db)):
    result = await signup_admin(db, payload)
    
    if hasattr(result, 'detail'):
        raise result
    
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
    
    return result

