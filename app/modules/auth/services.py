from app.modules.auth.schemas import Login
from sqlalchemy.orm import Session
from sqlalchemy import text
from .helpers import (
    verify_password,
    generate_access_token,
    generate_refresh_token,
    hash_password
)
from ...helpers.responses import success_response, error_response


async def login_farmer(db: Session, payload: Login):
    try:
        query = text("SELECT farmer_id, username, password FROM farmer WHERE username = :username")
        result = db.execute(
            query,
            {"username": payload.username}
        ).mappings().fetchone()

        if result is None:
            return error_response(
                message="Invalid credentials",
                status_code=401
            )

        verified = verify_password(payload.password, result["password"])

        if not verified:
            return error_response(
                message="Invalid credentials",
                status_code=401
            )

        access_token = generate_access_token({
            "farmer_id": str(result["farmer_id"]),
            "username": result["username"]
        })

        refresh_token = generate_refresh_token({
            "farmer_id": str(result["farmer_id"]),
            "username": result["username"]
        })

        return success_response(
            message="Login successful",
            data={
                "farmer_id": str(result["farmer_id"]),
                "username": result["username"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
    
    except Exception:
        return error_response(
            message="Login failed"
        )


async def signup_farmer(db: Session, payload: Login):
    try:
        exists_query = text("SELECT 1 FROM farmer WHERE username = :username LIMIT 1")

        exists_result = db.execute(
            exists_query,
            {"username": payload.username}
        ).fetchone()

        if exists_result:
            return error_response(
                message="Username already exists",
                status_code=400
            )

        hashed_password = hash_password(payload.password)

        query = text("""
            INSERT INTO farmer (username, password)
            VALUES (:username, :password)
            RETURNING farmer_id, username
        """)

        result = db.execute(
            query,
            {
                "username": payload.username,
                "password": hashed_password
            }
        ).mappings().fetchone()

        db.commit()

        if result is None:
            return error_response(
                message="Signup failed"
            )

        access_token = generate_access_token({
            "farmer_id": str(result["farmer_id"]),
            "username": result["username"]
        })

        refresh_token = generate_refresh_token({
            "farmer_id": str(result["farmer_id"]),
            "username": result["username"]
        })

        return success_response(
            message="Signup successful",
            data={
                "farmer_id": str(result["farmer_id"]),
                "username": result["username"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
    
    except Exception:
        db.rollback()
        return error_response(
            message="Signup failed"
        )


async def login_admin(db: Session, payload: Login):
    try:
        query = text("SELECT admin_id, username, password FROM admin WHERE username = :username")
        result = db.execute(
            query,
            {"username": payload.username}
        ).mappings().fetchone()

        if result is None:
            return error_response(
                message="Invalid credentials",
                status_code=401
            )

        verified = verify_password(payload.password, result["password"])

        if not verified:
            return error_response(
                message="Invalid credentials",
                status_code=401
            )

        access_token = generate_access_token({
            "admin_id": str(result["admin_id"]),
            "username": result["username"]
        })

        refresh_token = generate_refresh_token({
            "admin_id": str(result["admin_id"]),
            "username": result["username"]
        })

        return success_response(
            message="Login successful",
            data={
                "admin_id": str(result["admin_id"]),
                "username": result["username"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
    
    except Exception:
        return error_response(
            message="Login failed"
        )


async def signup_admin(db: Session, payload: Login):
    try:
        hashed_password = hash_password(payload.password)

        query = text("""
            INSERT INTO admin (username, password)
            VALUES (:username, :password)
            RETURNING admin_id, username
        """)

        result = db.execute(
            query,
            {
                "username": payload.username,
                "password": hashed_password
            }
        ).mappings().fetchone()

        db.commit()

        if result is None:
            return error_response(
                message="Signup failed"
            )

        access_token = generate_access_token({
            "admin_id": str(result["admin_id"]),
            "username": result["username"]
        })

        refresh_token = generate_refresh_token({
            "admin_id": str(result["admin_id"]),
            "username": result["username"]
        })

        return success_response(
            message="Signup successful",
            data={
                "admin_id": str(result["admin_id"]),
                "username": result["username"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )
    
    except Exception:
        db.rollback()
        return error_response(
            message="Signup failed"
        )

