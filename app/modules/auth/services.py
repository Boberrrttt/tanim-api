from app.modules.auth.schemas import Login
from sqlalchemy.orm import Session
from sqlalchemy import text
from .helpers import verify_password, generate_access_token, generate_refresh_token, hash_password

async def login_farmer(db: Session, payload: Login) -> dict | None:
    query = text("SELECT farmer_id, username, password FROM farmer WHERE username = :username")
    result = db.execute(
        query, 
        {"username": payload.username}
    ).mappings().fetchone()
    verified = verify_password(payload.password, result['password']) 
    
    if not verified: 
        return None
    
    access_token = generate_access_token({
        "farmer_id": str(result['farmer_id']),
        "username": result['username']
    })
 
    refresh_token = generate_refresh_token({
        "farmer_id": str(result['farmer_id']),
        "username": result['username']
    })

    return {
        "farmer_id": str(result['farmer_id']),
        "username": result['username'],
        "access_token": access_token,
        "refresh_token": refresh_token
    }

async def signup_farmer(db: Session, payload: Login) -> dict | None:
    hashed_password = hash_password(payload.password)
    query = text("INSERT INTO farmer (username, password) VALUES (:username, :password) RETURNING farmer_id, username")

    result = db.execute(
        query, 
        {
            "username": payload.username, 
            "password": hashed_password
        }
    ).mappings().fetchone()
    db.commit()
    
    access_token = generate_access_token({
        "farmer_id": str(result['farmer_id']),
        "username": result['username']
    })
 
    refresh_token = generate_refresh_token({
        "farmer_id": str(result['farmer_id']),
        "username": result['username']
    })
    
    return {
        "farmer_id": str(result['farmer_id']),
        "username": result['username'],
        "access_token": access_token,
        "refresh_token": refresh_token
    }

async def login_admin(db: Session, payload: Login) -> dict | None:
    query = text("SELECT admin_id, username, password FROM admin WHERE username = :username")
    result = db.execute(
        query, 
        {"username": payload.username}
    ).mappings().fetchone()
    verified = verify_password(payload.password, result['password']) 
    
    if not verified: 
        return None
    
    access_token = generate_access_token({
        "admin_id": str(result['admin_id']),
        "username": result['username']
    })
 
    refresh_token = generate_refresh_token({
        "admin_id": str(result['admin_id']),
        "username": result['username']
    })

    return {
        "admin_id": str(result['admin_id']),
        "username": result['username'],
        "access_token": access_token,
        "refresh_token": refresh_token
    }