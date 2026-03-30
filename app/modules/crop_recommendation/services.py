import json
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.crop_recommendation.models import CropRecommendation
from app.modules.crop_recommendation.schemas import (
    CreateCropRecommendation,
    UpdateCropRecommendation,
)
from ...helpers.responses import error_response, success_response


def _utc_today_date():
    return datetime.now(timezone.utc).date()


def _as_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _probabilities_json(payload: CreateCropRecommendation | UpdateCropRecommendation) -> str:
    return json.dumps([p.model_dump() for p in payload.probabilities])


async def create(db: Session, body: CreateCropRecommendation):
    try:
        print(
            f"[crop_recommendation] POST /api/v1/crop-recommendations/ create "
            f"farm_id={body.farm_id!r} probability_count={len(body.probabilities)}"
        )
        created_at = body.created_at or datetime.now(timezone.utc)
        created_at = _as_utc(created_at)
        day = created_at.date()
        today = _utc_today_date()

        if day == today:
            dup = text("""
                SELECT 1 FROM crop_recommendation
                WHERE farm_id = :farm_id
                AND (created_at AT TIME ZONE 'UTC')::date = CAST(:today AS date)
                LIMIT 1
            """)
            if db.execute(
                dup, {"farm_id": body.farm_id, "today": today.isoformat()}
            ).fetchone():
                raise error_response(
                    message="A crop recommendation already exists for today for this farm; use PUT /api/v1/crop-recommendations/ to update.",
                    status_code=409,
                )

        probs = [p.model_dump() for p in body.probabilities]
        record = CropRecommendation(
            farm_id=body.farm_id,
            probabilities=probs,
            created_at=created_at,
            updated_at=created_at,
        )

        recommendation_id = str(uuid.uuid4())
        query = text("""
            INSERT INTO crop_recommendation (recommendation_id, farm_id, probabilities, created_at, updated_at)
            VALUES (:recommendation_id, :farm_id, CAST(:probabilities AS jsonb), :created_at, :updated_at)
        """)

        result = db.execute(
            query,
            {
                "recommendation_id": recommendation_id,
                "farm_id": body.farm_id,
                "probabilities": _probabilities_json(body),
                "created_at": created_at,
                "updated_at": created_at,
            },
        )

        if result.rowcount == 0:
            db.rollback()
            print(
                f"[crop_recommendation] POST /api/v1/crop-recommendations/ create failed "
                f"farm_id={body.farm_id!r} reason=no_rows_inserted"
            )
            raise error_response(
                message="Failed to create crop recommendation - no rows affected"
            )

        db.commit()

        data = record.to_dict()
        data["recommendation_id"] = recommendation_id

        return success_response(
            message="Crop recommendation created successfully",
            data=data,
        )

    except HTTPException as exc:
        db.rollback()
        print(
            f"[crop_recommendation] POST /api/v1/crop-recommendations/ create rejected "
            f"farm_id={body.farm_id!r} status={exc.status_code} detail={exc.detail!r}"
        )
        raise
    except IntegrityError as e:
        db.rollback()
        orig = str(e.orig) if getattr(e, "orig", None) else str(e)
        print(
            f"[crop_recommendation] POST /api/v1/crop-recommendations/ create integrity_error "
            f"farm_id={body.farm_id!r} db_message={orig!r}"
        )
        if "farm_id" in orig and "farm" in orig.lower():
            raise error_response(
                message="Invalid farm_id: that farm does not exist in the database.",
                status_code=400,
                details={"database": orig},
            )
        raise error_response(
            message="Could not save crop recommendation (database constraint).",
            status_code=400,
            details={"database": orig},
        )
    except Exception as e:
        db.rollback()
        print(
            f"[crop_recommendation] POST /api/v1/crop-recommendations/ create failed "
            f"farm_id={body.farm_id!r}: {e!r}"
        )
        raise error_response(
            message=f"Failed to create crop recommendation: {str(e)}"
        )


async def update_today(db: Session, payload: UpdateCropRecommendation):
    try:
        print(
            f"[crop_recommendation] PUT /api/v1/crop-recommendations/ update_today "
            f"farm_id={payload.farm_id!r}"
        )
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
            UPDATE crop_recommendation
            SET probabilities = CAST(:probabilities AS jsonb),
                updated_at = :updated_at
            WHERE recommendation_id = (
                SELECT recommendation_id FROM crop_recommendation
                WHERE farm_id = :farm_id
                AND (created_at AT TIME ZONE 'UTC')::date = CAST(:today AS date)
                ORDER BY created_at DESC
                LIMIT 1
            )
            RETURNING recommendation_id, farm_id, probabilities, created_at, updated_at
        """)

        row = db.execute(
            query,
            {
                "farm_id": payload.farm_id,
                "today": today.isoformat(),
                "probabilities": _probabilities_json(payload),
                "updated_at": updated_at,
            },
        ).fetchone()

        if row is None:
            db.rollback()
            print(
                f"[crop_recommendation] PUT /api/v1/crop-recommendations/ no_row_for_today "
                f"farm_id={payload.farm_id!r} utc_date={today.isoformat()!r}"
            )
            raise error_response(
                message="No crop recommendation found for today for this farm; use POST to create one.",
                status_code=404,
            )

        db.commit()

        probs = row.probabilities
        if isinstance(probs, str):
            probs = json.loads(probs)

        record = CropRecommendation(
            farm_id=row.farm_id,
            probabilities=probs,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
        data = record.to_dict()
        data["recommendation_id"] = row.recommendation_id

        return success_response(
            message="Crop recommendation updated successfully",
            data=data,
        )

    except HTTPException as exc:
        db.rollback()
        print(
            f"[crop_recommendation] PUT /api/v1/crop-recommendations/ update rejected "
            f"farm_id={payload.farm_id!r} status={exc.status_code} detail={exc.detail!r}"
        )
        raise
    except IntegrityError as e:
        db.rollback()
        orig = str(e.orig) if getattr(e, "orig", None) else str(e)
        print(
            f"[crop_recommendation] PUT /api/v1/crop-recommendations/ integrity_error "
            f"farm_id={payload.farm_id!r} db_message={orig!r}"
        )
        raise error_response(
            message="Could not update crop recommendation (database constraint).",
            status_code=400,
            details={"database": orig},
        )
    except Exception as e:
        db.rollback()
        print(
            f"[crop_recommendation] PUT /api/v1/crop-recommendations/ update failed "
            f"farm_id={payload.farm_id!r}: {e!r}"
        )
        raise error_response(
            message=f"Failed to update crop recommendation: {str(e)}"
        )


async def get_by_farm_id(db: Session, farm_id: str):
    try:
        print(
            f"[crop_recommendation] GET /api/v1/crop-recommendations/{{farm_id}} "
            f"farm_id={farm_id!r}"
        )
        query = text("""
            SELECT * FROM crop_recommendation
            WHERE farm_id = :farm_id
            ORDER BY created_at DESC
        """)

        result = db.execute(query, {"farm_id": farm_id})

        if result.rowcount == 0:
            return success_response(
                message="No crop recommendations found for this farm",
                data=[],
            )

        rows = []
        for row in result:
            probs = row.probabilities
            if isinstance(probs, str):
                probs = json.loads(probs)
            record = CropRecommendation(
                farm_id=row.farm_id,
                probabilities=probs,
                created_at=row.created_at,
                updated_at=getattr(row, "updated_at", None),
            )
            item = record.to_dict()
            item["recommendation_id"] = row.recommendation_id
            rows.append(item)

        return success_response(
            message="Crop recommendations retrieved successfully",
            data=rows,
        )

    except Exception as e:
        print(
            f"[crop_recommendation] GET /api/v1/crop-recommendations/{{farm_id}} failed "
            f"farm_id={farm_id!r}: {e!r}"
        )
        raise error_response(
            message=f"Failed to retrieve crop recommendations: {str(e)}"
        )
