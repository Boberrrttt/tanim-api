from .models import Farmer
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..auth.helpers import hash_password
from ...helpers.responses import success_response, error_response
import uuid

async def get_all(db: Session):
    try:
        query = text("""
            SELECT f.farmer_id, f.username, f.password, f.first_name, f.last_name, f.created_at,
                   (SELECT farm_id FROM farm WHERE farmer_id = f.farmer_id LIMIT 1) as farm_id
            FROM farmer f
        """)
        result = db.execute(query)

        farmers = []
        for row in result:
            farm_id = str(row.farm_id) if row.farm_id else None
            farmer = Farmer(
                farmer_id=str(row.farmer_id),
                username=row.username,
                password=row.password,
                first_name=getattr(row, "first_name", None) or "",
                last_name=getattr(row, "last_name", None) or "",
                farm_id=farm_id,
                created_at=row.created_at
            )
            farmers.append(farmer.to_public_dict())

        return success_response(
            message="Farmers retrieved successfully",
            data=farmers,
            total=len(farmers)
        )

    except Exception:
        return error_response(
            message="Failed to retrieve farmers"
        )

async def update_farmer(db: Session, payload: Farmer):
    try:
        update_fields = []
        params = {"farmer_id": payload.farmer_id}

        if payload.username:
            update_fields.append("username = :username")
            params["username"] = payload.username

        if payload.password:
            hashed_password = hash_password(payload.password)
            update_fields.append("password = :password")
            params["password"] = hashed_password

        if payload.first_name:
            update_fields.append("first_name = :first_name")
            params["first_name"] = payload.first_name

        if payload.last_name:
            update_fields.append("last_name = :last_name")
            params["last_name"] = payload.last_name

        if payload.farm_id:
            farm_id_uuid = uuid.UUID(payload.farm_id) if isinstance(payload.farm_id, str) else payload.farm_id
            update_fields.append("farm_id = :farm_id")
            params["farm_id"] = str(farm_id_uuid)

        if not update_fields:
            return error_response(
                message="No fields to update",
                status_code=400
            )

        query = text(f"""
            UPDATE farmer
            SET {', '.join(update_fields)}
            WHERE farmer_id = :farmer_id
            RETURNING farmer_id, username, first_name, last_name, farm_id, created_at
        """)

        result = db.execute(query, params).mappings().fetchone()

        if result is None:
            return error_response(
                message="Farmer not found",
                status_code=404
            )

        db.commit()

        return success_response(
            message="Farmer updated successfully",
            data={
                "farmer_id": str(result["farmer_id"]),
                "username": result["username"],
                "first_name": result["first_name"],
                "last_name": result["last_name"],
                "farm_id": result["farm_id"]
            }
        )
    
    except ValueError as e:
        return error_response(
            message=str(e),
            status_code=400
        )
    except Exception:
        db.rollback()
        return error_response(
            message="Failed to update farmer"
        )
