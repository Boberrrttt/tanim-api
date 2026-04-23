from datetime import datetime, timezone
import uuid

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
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
        print(
            f"[soil_health_test] POST /api/v1/test/ create farm_id={soil_health_test.farm_id!r}"
        )
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
            created_at=created_at,
            updated_at=created_at,
        )

        test_id = str(uuid.uuid4())

        query = text("""
            INSERT INTO soil_health_test (test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity, temperature, moisture, created_at, updated_at)
            VALUES (:test_id, :farm_id, :nitrogen, :phosphorus, :potassium, :ph, :salinity, :temperature, :moisture, :created_at, :updated_at)
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
            'created_at': created_at.isoformat(),
            'updated_at': created_at.isoformat(),
        })
        
        if result.rowcount == 0:
            db.rollback()
            print(
                f"[soil_health_test] POST /api/v1/test/ create failed farm_id={soil_health_test.farm_id!r} "
                "reason=no_rows_inserted"
            )
            raise error_response(
                message="Failed to create soil health test - no rows affected"
            )
        
        db.commit()

        test_data = test.to_dict()
        test_data['test_id'] = test_id
        
        return success_response(
            message="Soil health test created successfully",
            data=test_data
        )

    except HTTPException as exc:
        db.rollback()
        print(
            f"[soil_health_test] POST /api/v1/test/ create rejected farm_id={soil_health_test.farm_id!r} "
            f"status={exc.status_code} detail={exc.detail!r}"
        )
        raise
    except IntegrityError as e:
        db.rollback()
        orig = str(e.orig) if getattr(e, "orig", None) else str(e)
        print(
            f"[soil_health_test] POST /api/v1/test/ create integrity_error farm_id={soil_health_test.farm_id!r} "
            f"db_message={orig!r}"
        )
        if "farm_id" in orig and "farm" in orig.lower():
            raise error_response(
                message="Invalid farm_id: that farm does not exist in the database.",
                status_code=400,
                details={"database": orig},
            )
        raise error_response(
            message="Could not save soil health test (database constraint).",
            status_code=400,
            details={"database": orig},
        )
    except Exception as e:
        db.rollback()
        print(
            f"[soil_health_test] POST /api/v1/test/ create failed farm_id={soil_health_test.farm_id!r}: {e!r}"
        )
        raise error_response(
            message=f"Failed to create soil health test: {str(e)}"
        )


async def update_today(db: Session, payload: UpdateSoilHealthTest):
    try:
        print(f"[soil_health_test] PUT /api/v1/test/ update_today farm_id={payload.farm_id!r}")
        today = _utc_today_date()
        if payload.created_at is not None:
            ref = _as_utc(payload.created_at)
            if ref.date() != today:
                raise error_response(
                    message="PUT only updates today's record for the farm; when created_at is not today, use POST to create a new row.",
                    status_code=400,
                )

        updated_at = datetime.now(timezone.utc)

        query = text("""
            UPDATE soil_health_test
            SET nitrogen = :nitrogen,
                phosphorus = :phosphorus,
                potassium = :potassium,
                ph = :ph,
                salinity = :salinity,
                temperature = :temperature,
                moisture = :moisture,
                updated_at = :updated_at
            WHERE test_id = (
                SELECT test_id FROM soil_health_test
                WHERE farm_id = :farm_id
                AND (created_at AT TIME ZONE 'UTC')::date = CAST(:today AS date)
                ORDER BY created_at DESC
                LIMIT 1
            )
            RETURNING test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity, temperature, moisture, created_at, updated_at
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
            "updated_at": updated_at.isoformat(),
        }).fetchone()

        if row is None:
            db.rollback()
            print(
                f"[soil_health_test] PUT /api/v1/test/ no_row_for_today farm_id={payload.farm_id!r} "
                f"utc_date={today.isoformat()!r}"
            )
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
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
        test_data = test.to_dict()
        test_data["test_id"] = row.test_id

        return success_response(
            message="Soil health test updated successfully",
            data=test_data,
        )

    except HTTPException as exc:
        db.rollback()
        print(
            f"[soil_health_test] PUT /api/v1/test/ update rejected farm_id={payload.farm_id!r} "
            f"status={exc.status_code} detail={exc.detail!r}"
        )
        raise
    except IntegrityError as e:
        db.rollback()
        orig = str(e.orig) if getattr(e, "orig", None) else str(e)
        print(
            f"[soil_health_test] PUT /api/v1/test/ integrity_error farm_id={payload.farm_id!r} "
            f"db_message={orig!r}"
        )
        raise error_response(
            message="Could not update soil health test (database constraint).",
            status_code=400,
            details={"database": orig},
        )
    except Exception as e:
        db.rollback()
        print(f"[soil_health_test] PUT /api/v1/test/ update failed farm_id={payload.farm_id!r}: {e!r}")
        raise error_response(
            message=f"Failed to update soil health test: {str(e)}"
        )


async def get_by_farm_id(db: Session, farm_id: str):
    try:
        print(f"[soil_health_test] GET /api/v1/test/{{farm_id}} farm_id={farm_id!r}")
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
                created_at=row.created_at,
                updated_at=getattr(row, "updated_at", None),
            )
            test_data = test.to_dict()
            test_data['test_id'] = row.test_id
            tests.append(test_data)
        
        return success_response(
            message="Soil health tests retrieved successfully",
            data=tests,
        )
    
    except Exception as e:
        print(f"[soil_health_test] GET /api/v1/test/{{farm_id}} failed farm_id={farm_id!r}: {e!r}")
        raise error_response(
            message=f"Failed to retrieve soil health tests: {str(e)}"
        )


async def upsert_today_after_ml(db: Session, payload: UpdateSoilHealthTest):
    """
    Insert or update a single `soil_health_test` row for the current UTC calendar day.
    Used by the mobile app after a successful `GET` from the model's pending cache.
    Commits the transaction; returns the row like `update_today`.
    """
    try:
        print(f"[soil_health_test] PUT /api/v1/test/upsert after_ml farm_id={payload.farm_id!r}")
        reference_time = datetime.now(timezone.utc)
        upsert_soil_health_for_calendar_day_no_commit(
            db,
            payload.farm_id,
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            ph=payload.ph,
            salinity=payload.salinity,
            temperature=payload.temperature,
            moisture=payload.moisture,
            reference_time=reference_time,
        )
        db.commit()

        today = _utc_today_date()
        read = text(
            """
            SELECT test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity,
                temperature, moisture, created_at, updated_at
            FROM soil_health_test
            WHERE farm_id = :farm_id
            AND (created_at AT TIME ZONE 'UTC')::date = CAST(:today AS date)
            ORDER BY created_at DESC
            LIMIT 1
            """
        )
        row = db.execute(
            read, {"farm_id": payload.farm_id, "today": today.isoformat()}
        ).fetchone()
        if row is None:
            raise error_response(
                message="Upsert did not return a row for today (unexpected).",
                status_code=500,
            )

        test = SoilHealthTest(
            nitrogen=row.nitrogen,
            phosphorus=row.phosphorus,
            potassium=row.potassium,
            ph=row.ph,
            salinity=row.salinity,
            temperature=row.temperature,
            moisture=row.moisture,
            farm_id=row.farm_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
        test_data = test.to_dict()
        test_data["test_id"] = row.test_id

        return success_response(
            message="Soil health test saved for today",
            data=test_data,
        )
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError as e:
        db.rollback()
        orig = str(e.orig) if getattr(e, "orig", None) else str(e)
        print(
            f"[soil_health_test] PUT /api/v1/test/upsert integrity_error farm_id={payload.farm_id!r} "
            f"db_message={orig!r}"
        )
        raise error_response(
            message="Could not save soil health test (database constraint).",
            status_code=400,
            details={"database": orig},
        )
    except Exception as e:
        db.rollback()
        print(
            f"[soil_health_test] PUT /api/v1/test/upsert failed farm_id={payload.farm_id!r}: {e!r}"
        )
        raise error_response(message=f"Failed to save soil health test: {str(e)}")


def upsert_soil_health_for_calendar_day_no_commit(
    db: Session,
    farm_id: str,
    *,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph: float,
    salinity: float,
    temperature: float,
    moisture: float,
    reference_time: datetime,
) -> None:
    """
    Insert or update `soil_health_test` for the UTC calendar day of `reference_time`.
    Does not commit — caller owns the transaction (e.g. start farming).
    """
    reference_time = _as_utc(reference_time)
    day_iso = reference_time.date().isoformat()
    updated_at = datetime.now(timezone.utc)

    find = text(
        """
        SELECT test_id FROM soil_health_test
        WHERE farm_id = :farm_id
        AND (created_at AT TIME ZONE 'UTC')::date = CAST(:day AS date)
        ORDER BY created_at DESC
        LIMIT 1
        """
    )
    row = db.execute(find, {"farm_id": farm_id, "day": day_iso}).fetchone()

    params = {
        "nitrogen": nitrogen,
        "phosphorus": phosphorus,
        "potassium": potassium,
        "ph": ph,
        "salinity": salinity,
        "temperature": temperature,
        "moisture": moisture,
    }

    if row is not None:
        tid = row.test_id
        db.execute(
            text(
                """
                UPDATE soil_health_test SET
                    nitrogen = :nitrogen,
                    phosphorus = :phosphorus,
                    potassium = :potassium,
                    ph = :ph,
                    salinity = :salinity,
                    temperature = :temperature,
                    moisture = :moisture,
                    updated_at = :updated_at
                WHERE test_id = :test_id
                """
            ),
            {
                **params,
                "updated_at": updated_at.isoformat(),
                "test_id": tid,
            },
        )
        return

    test_id = str(uuid.uuid4())
    db.execute(
        text(
            """
            INSERT INTO soil_health_test (
                test_id, farm_id, nitrogen, phosphorus, potassium, ph, salinity,
                temperature, moisture, created_at, updated_at
            )
            VALUES (
                :test_id, :farm_id, :nitrogen, :phosphorus, :potassium, :ph, :salinity,
                :temperature, :moisture, :created_at, :updated_at
            )
            """
        ),
        {
            **params,
            "test_id": test_id,
            "farm_id": farm_id,
            "created_at": reference_time.isoformat(),
            "updated_at": updated_at.isoformat(),
        },
    )