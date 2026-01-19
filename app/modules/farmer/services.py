from .models import Farmer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import text
from ..auth.helpers import hash_password
import uuid

async def update_farmer(db: Session, payload: Farmer) -> Farmer:
    update_fields = []
    params = {"farmer_id": payload.farmer_id}
    
    if payload.username:
        update_fields.append("username = :username")
        params["username"] = payload.username
    
    if payload.password:
        hashed_password = hash_password(payload.password)
        update_fields.append("password = :password")
        params["password"] = hashed_password
    
    if payload.farm_id:
        farm_id_uuid = uuid.UUID(payload.farm_id) if isinstance(payload.farm_id, str) else payload.farm_id
        update_fields.append("farm_id = :farm_id")
        params["farm_id"] = farm_id_uuid

    if not update_fields:
        raise ValueError("No fields to update")
    
    query = text(f"""
        UPDATE farmer
        SET {', '.join(update_fields)}
        WHERE farmer_id = :farmer_id
        RETURNING farmer_id, username, farm_id, created_at
    """)
    
    result = db.execute(query, params).mappings().fetchone()
    db.commit()
    
    return Farmer(
        farmer_id=result["farmer_id"],
        username=result["username"],
        farm_id=result["farm_id"],
        created_at=result["created_at"]
    )