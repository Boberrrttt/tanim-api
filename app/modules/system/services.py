from sqlalchemy.orm import Session
from sqlalchemy import text
from .schemas import CreateSystem, UpdateBatteryStatus
from ...helpers.responses import success_response, error_response

async def create(db: Session, payload: CreateSystem):
    try:
        query = text("INSERT INTO tanim_system (battery_status) VALUES (:battery_status)")
        result = db.execute(query, {
            "battery_status": payload.battery_status
        })
        
        if result.rowcount == 0:
            db.rollback()
            return error_response(
                message="Failed to create system"
            )
        
        db.commit()

        return success_response(
            message="System created successfully",
            data={
                "battery_status": payload.battery_status
            }
        )
    except Exception:
        db.rollback()
        return error_response(
            message="Failed to create system"
        )

async def update(db: Session, payload: UpdateBatteryStatus):
    try:
        query = text("UPDATE tanim_system SET battery_status = :battery_status WHERE system_id = :system_id")
        result = db.execute(query, {
            "battery_status": payload.battery_status,
            "system_id": payload.system_id
        })
        
        if result.rowcount == 0:
            db.rollback()
            return error_response(
                message="System not found"
            )
        
        db.commit()

        return success_response(
            message="Battery status updated successfully",
            data={
                "system_id": payload.system_id,
                "battery_status": payload.battery_status
            }
        )
    except Exception:
        db.rollback()
        return error_response(
            message="Failed to update battery status"
        )