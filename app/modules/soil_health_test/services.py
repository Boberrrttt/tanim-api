from datetime import datetime, timezone
import uuid

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.soil_health_test.models import SoilHealthTest
from app.modules.soil_health_test.schemas import CreateSoilHealthTest, UpdateSoilHealthTest
from ...helpers.responses import error_response, success_response


def _utc_today_date():
    return datetime.now(timezone.utc).date()


def _as_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


async def create(db: Session, soil_health_test: CreateSoilHealthTest):
    try:
        created_at = soil_health_test.created_at or datetime.now(timezone.utc)
        created_at = _as_utc(created_at)
        day = created_at.date()
        today = _utc_today_date()

        if day == today:
            dup = text("""
                SELECT 1 FROM soil_health_test
                WHERE farm_id = :farm_id
                AND (created_at AT TIME ZONE 'UTC')::date = CAST(:today AS date)
                LIMIT 1
            """)
            if db.execute(dup, {"farm_id": soil_health_test.farm_id, "today": today.isoformat()}).fetchone():
                raise error_response(
                    message="A soil health test already exists for today for this farm; use PUT /api/v1/test/ to update.",
                    status_code=409,
                )

        test = SoilHealthTest(
            nitrogen=soil_health_test.nitrogen,
            phosphorus=soil_health_test.phosphorus,
            potassium=soil_health_test.potassium,
            ph=soil_health_test.ph,
            salinity=soil_health_test.salinity,
            temperature=soil_health_test.temperature,
            moisture=soil_health_test.moisture,
            farm_id=soil_health_test.farm_id,
            classification=soil_health_test.classification,
            created_at=created_at,
        )

        test_id = str(uuid.uuid4())

        query = text("""
            INSERT INTO soil_health_test (test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity, temperature, moisture, classification, created_at)
            VALUES (:test_id, :farm_id, :nitrogen, :phosphorus, :potassium, :ph, :salinity, :temperature, :moisture, :classification, :created_at)
        """)

        result = db.execute(query, {
            'test_id': test_id,
            'farm_id': soil_health_test.farm_id,
            'nitrogen': soil_health_test.nitrogen,
            'phosphorus': soil_health_test.phosphorus,
            'potassium': soil_health_test.potassium,
            'ph': soil_health_test.ph,
            'salinity': soil_health_test.salinity,
            'temperature': soil_health_test.temperature,
            'moisture': soil_health_test.moisture,
            'classification': soil_health_test.classification,
            'created_at': created_at.isoformat(),
        })
        
        if result.rowcount == 0:
            db.rollback()
            return error_response(
                message="Failed to create soil health test - no rows affected"
            )
        
        db.commit()

        test_data = test.to_dict()
        test_data['test_id'] = test_id
        
        return success_response(
            message="Soil health test created successfully",
            data=test_data
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Error creating soil health test: {str(e)}")
        return error_response(
            message=f"Failed to create soil health test: {str(e)}"
        )


async def update_today(db: Session, payload: UpdateSoilHealthTest):
    try:
        today = _utc_today_date()
        if payload.created_at is not None:
            ref = _as_utc(payload.created_at)
            if ref.date() != today:
                raise error_response(
                    message="PUT only updates today's record for the farm; when created_at is not today, use POST to create a new row.",
                    status_code=400,
                )

        query = text("""
            UPDATE soil_health_test
            SET nitrogen = :nitrogen,
                phosphorus = :phosphorus,
                potassium = :potassium,
                ph = :ph,
                salinity = :salinity,
                temperature = :temperature,
                moisture = :moisture,
                classification = :classification
            WHERE test_id = (
                SELECT test_id FROM soil_health_test
                WHERE farm_id = :farm_id
                AND (created_at AT TIME ZONE 'UTC')::date = CAST(:today AS date)
                ORDER BY created_at DESC
                LIMIT 1
            )
            RETURNING test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity, temperature, moisture, classification, created_at
        """)

        row = db.execute(query, {
            "farm_id": payload.farm_id,
            "today": today.isoformat(),
            "nitrogen": payload.nitrogen,
            "phosphorus": payload.phosphorus,
            "potassium": payload.potassium,
            "ph": payload.ph,
            "salinity": payload.salinity,
            "temperature": payload.temperature,
            "moisture": payload.moisture,
            "classification": payload.classification,
        }).fetchone()

        if row is None:
            db.rollback()
            raise error_response(
                message="No soil health test found for today for this farm; use POST to create one.",
                status_code=404,
            )

        db.commit()

        test = SoilHealthTest(
            nitrogen=row.nitrogen,
            phosphorus=row.phosphorus,
            potassium=row.potassium,
            ph=row.ph,
            salinity=row.salinity,
            temperature=row.temperature,
            moisture=row.moisture,
            farm_id=row.farm_id,
            classification=row.classification,
            created_at=row.created_at,
        )
        test_data = test.to_dict()
        test_data["test_id"] = row.test_id

        return success_response(
            message="Soil health test updated successfully",
            data=test_data,
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating soil health test: {str(e)}")
        return error_response(
            message=f"Failed to update soil health test: {str(e)}"
        )


async def get_by_farm_id(db: Session, farm_id: str):
    try:
        query = text("""
            SELECT * FROM soil_health_test 
            WHERE farm_id = :farm_id 
            ORDER BY created_at DESC
        """)
        
        result = db.execute(query, {'farm_id': farm_id})
        
        if result.rowcount == 0:
            return success_response(
                message="No soil health tests found for this farm",
                data=[],
            )
        
        tests = []
        for row in result:
            test = SoilHealthTest(
                nitrogen=row.nitrogen,
                phosphorus=row.phosphorus,
                potassium=row.potassium,
                ph=row.ph,
                salinity=row.salinity,
                temperature=row.temperature,
                moisture=row.moisture,
                farm_id=row.farm_id,
                classification=row.classification,
                created_at=row.created_at
            )
            test_data = test.to_dict()
            test_data['test_id'] = row.test_id
            tests.append(test_data)
        
        return success_response(
            message="Soil health tests retrieved successfully",
            data=tests,
        )
    
    except Exception as e:
        print(f"Error retrieving soil health tests: {str(e)}")
        return error_response(
            message=f"Failed to retrieve soil health tests: {str(e)}"
        )