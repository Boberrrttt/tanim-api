import logging
from app.modules.auth.schemas import Login, SignupFarmer
from sqlalchemy.orm import Session
from sqlalchemy import text
from .helpers import (
    verify_password,
    generate_access_token,
    generate_refresh_token,
    hash_password
)
from ...helpers.responses import success_response, error_response

logger = logging.getLogger(__name__)


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


async def signup_farmer(db: Session, payload: SignupFarmer):
    try:
        logger.info("Signup attempt: username=%r, farm_id=%r", payload.username, payload.farm_id)

        exists_query = text("SELECT 1 FROM farmer WHERE username = :username LIMIT 1")
        exists_result = db.execute(
            exists_query,
            {"username": payload.username}
        ).fetchone()

        if exists_result:
            logger.warning("Signup rejected: username %r already exists", payload.username)
            return error_response(
                message="Username already exists",
                status_code=400
            )

        hashed_password = hash_password(payload.password)

        if payload.farm_id:
            query = text("""
                INSERT INTO farmer (username, password)
                VALUES (:username, :password)
                RETURNING farmer_id, username
            """)
            params = {
                "username": payload.username,
                "password": hashed_password
            }
        else:
            query = text("""
                INSERT INTO farmer (username, password)
                VALUES (:username, :password)
                RETURNING farmer_id, username
            """)
            params = {
                "username": payload.username,
                "password": hashed_password
            }

        result = db.execute(query, params).mappings().fetchone()

        if result is None:
            logger.error("Signup failed: INSERT returned no row for username=%r", payload.username)
            return error_response(
                message="Signup failed"
            )

        farmer_id = str(result["farmer_id"])

        # If farm_id provided, assign the new farmer_id to the farm
        if payload.farm_id:
            update_farm_query = text("""
                UPDATE farm
                SET farmer_id = :farmer_id
                WHERE farm_id = :farm_id
            """)
            db.execute(update_farm_query, {
                "farmer_id": farmer_id,
                "farm_id": payload.farm_id
            })

        db.commit()

        access_token = generate_access_token({
            "farmer_id": farmer_id,
            "username": result["username"]
        })
        refresh_token = generate_refresh_token({
            "farmer_id": farmer_id,
            "username": result["username"]
        })

        return success_response(
            message="Signup successful",
            data={
                "farmer_id": farmer_id,
                "username": result["username"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        )

    except Exception as e:
        db.rollback()
        logger.exception("Signup failed for username=%r: %s", payload.username, e)
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

