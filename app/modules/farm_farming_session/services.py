import json
import logging
import math
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.modules.farm_farming_session.schemas import StartFarmingSessionBody
from app.modules.soil_health_test.services import upsert_soil_health_for_calendar_day_no_commit
from ...helpers.responses import error_response, success_response

logger = logging.getLogger(__name__)


def _as_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _verify_farm_owner(db: Session, farm_id: str, farmer_id: str) -> bool:
    q = text(
        """
        SELECT 1 FROM farm
        WHERE farm_id = :farm_id AND farmer_id = :farmer_id
        LIMIT 1
        """
    )
    return db.execute(q, {"farm_id": farm_id, "farmer_id": farmer_id}).fetchone() is not None


def _row_to_dict(row) -> dict[str, Any]:
    m = row._mapping
    out: dict[str, Any] = {}
    for k in m.keys():
        v = m[k]
        if k in ("soil_snapshot", "fertilizer_recommendation", "top_crop_probabilities"):
            if v is not None and isinstance(v, str):
                try:
                    out[k] = json.loads(v)
                except json.JSONDecodeError:
                    out[k] = v
            else:
                out[k] = v
        elif k in ("created_at", "started_at", "ended_at") and v is not None:
            out[k] = v.isoformat() if hasattr(v, "isoformat") else str(v)
        else:
            out[k] = v

    # Older rows: started_at / selected_crop
    if "started_at" in m and "created_at" not in m:
        v = m["started_at"]
        if v is not None:
            out["created_at"] = v.isoformat() if hasattr(v, "isoformat") else str(v)
    if "selected_crop" in m and "selected_crops" not in m:
        out["selected_crops"] = m["selected_crop"]

    created = out.get("created_at")
    started = out.get("started_at")
    if created and not started:
        out["started_at"] = created
    elif started and not created:
        out["created_at"] = started

    crops = out.get("selected_crops")
    if crops is not None:
        out.setdefault("selected_crop", crops)

    return out


def _float_from_snapshot(snapshot: dict[str, Any], key: str, default: float = 0.0) -> float:
    v = snapshot.get(key, default)
    if isinstance(v, (int, float)) and math.isfinite(float(v)):
        return float(v)
    try:
        x = float(v)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def _soil_metrics_from_features_or_snapshot(
    features: list[float] | None,
    soil_snapshot: dict[str, Any],
) -> dict[str, float]:
    """
    Prefer ML `features`: [0]=N, [1]=P, [2]=K, [3]=pH, [4]=temp, [5]=moisture, [6]=EC (salinity).
    """
    if isinstance(features, list) and len(features) >= 6:
        try:
            f = [float(x) for x in features[:7]]
        except (TypeError, ValueError):
            f = []
        if len(f) >= 6 and all(math.isfinite(x) for x in f[:6]):
            salinity = f[6] if len(f) > 6 and math.isfinite(f[6]) else 0.0
            return {
                "nitrogen": f[0],
                "phosphorus": f[1],
                "potassium": f[2],
                "ph": f[3],
                "temperature": f[4],
                "moisture": f[5],
                "salinity": salinity,
            }
    return {
        "nitrogen": _float_from_snapshot(soil_snapshot, "nitrogen"),
        "phosphorus": _float_from_snapshot(soil_snapshot, "phosphorus"),
        "potassium": _float_from_snapshot(soil_snapshot, "potassium"),
        "ph": _float_from_snapshot(soil_snapshot, "ph"),
        "temperature": _float_from_snapshot(soil_snapshot, "temperature"),
        "moisture": _float_from_snapshot(soil_snapshot, "moisture"),
        "salinity": _float_from_snapshot(soil_snapshot, "salinity"),
    }


def _reference_time_for_soil_row(
    soil_snapshot: dict[str, Any], fallback: datetime
) -> datetime:
    raw = soil_snapshot.get("received_at")
    if isinstance(raw, str) and raw.strip():
        s = raw.strip().replace("Z", "+00:00")
        try:
            dt = datetime.fromisoformat(s)
            return _as_utc(dt)
        except ValueError:
            pass
    return fallback


async def start_farming_session(db: Session, body: StartFarmingSessionBody):
    try:
        if not _verify_farm_owner(db, body.farm_id, body.farmer_id):
            raise error_response(
                message="Farm not found or farmer_id does not own this farm.",
                status_code=403,
            )

        lat, lon = body.latitude, body.longitude
        if lat is not None and lon is not None:
            if not all(
                isinstance(x, (int, float)) and math.isfinite(float(x)) for x in (lat, lon)
            ):
                raise error_response(
                    message="latitude and longitude must be finite numbers when provided.",
                    status_code=400,
                )
            db.execute(
                text(
                    """
                    UPDATE farm
                    SET latitude = :lat, longitude = :lon
                    WHERE farm_id = :farm_id AND farmer_id = :farmer_id
                    """
                ),
                {
                    "lat": float(lat),
                    "lon": float(lon),
                    "farm_id": body.farm_id,
                    "farmer_id": body.farmer_id,
                },
            )

        created_at = body.started_at or datetime.now(timezone.utc)
        created_at = _as_utc(created_at)

        top_json = json.dumps(
            [p.model_dump() for p in body.top_crop_probabilities]
            if body.top_crop_probabilities
            else []
        )
        fert_json = json.dumps(body.fertilizer_recommendation)
        soil_json = json.dumps(body.soil_snapshot)
        selected_crop_val = body.selected_crop.strip()

        # End any still-active session for this farm (keeps history); then insert a new row.
        db.execute(
            text(
                """
                UPDATE farm_farming_session
                SET ended_at = :ended_at
                WHERE farm_id = :farm_id
                  AND farmer_id = :farmer_id
                  AND ended_at IS NULL
                """
            ),
            {
                "farm_id": body.farm_id,
                "farmer_id": body.farmer_id,
                "ended_at": created_at,
            },
        )
        insert_row = text(
            """
            INSERT INTO farm_farming_session (
                farm_id, farmer_id, selected_crop,
                soil_snapshot, fertilizer_recommendation,
                top_crop_probabilities, cycle_start_date, created_at
            )
            VALUES (
                :farm_id, :farmer_id, :selected_crop,
                CAST(:soil_snapshot AS jsonb),
                CAST(:fertilizer_recommendation AS jsonb),
                CAST(:top_crop_probabilities AS jsonb),
                :cycle_start_date, :created_at
            )
            """
        )
        db.execute(
            insert_row,
            {
                "farm_id": body.farm_id,
                "farmer_id": body.farmer_id,
                "selected_crop": selected_crop_val,
                "soil_snapshot": soil_json,
                "fertilizer_recommendation": fert_json,
                "top_crop_probabilities": top_json,
                "cycle_start_date": body.cycle_start_date,
                "created_at": created_at,
            },
        )

        snap = body.soil_snapshot if isinstance(body.soil_snapshot, dict) else {}
        feats = body.features if isinstance(body.features, list) else None
        metrics = _soil_metrics_from_features_or_snapshot(feats, snap)
        ref_soil = _reference_time_for_soil_row(snap, created_at)
        upsert_soil_health_for_calendar_day_no_commit(
            db,
            body.farm_id,
            nitrogen=metrics["nitrogen"],
            phosphorus=metrics["phosphorus"],
            potassium=metrics["potassium"],
            ph=metrics["ph"],
            salinity=metrics["salinity"],
            temperature=metrics["temperature"],
            moisture=metrics["moisture"],
            reference_time=ref_soil,
        )

        db.commit()

        row = db.execute(
            text(
                """
                SELECT * FROM farm_farming_session
                WHERE farm_id = :farm_id AND ended_at IS NULL
                ORDER BY created_at DESC
                LIMIT 1
                """
            ),
            {"farm_id": body.farm_id},
        ).fetchone()
        if not row:
            raise error_response(
                message="Farming session was not persisted.",
                status_code=500,
            )
        data = _row_to_dict(row)
        return success_response(message="Farming session saved", data=data)
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.exception("start_farming_session failed: %s", e)
        raise error_response(message=f"Could not save farming session: {e!s}")


async def get_session_by_farm_id(db: Session, farm_id: str):
    try:
        q = text(
            """
            SELECT * FROM farm_farming_session
            WHERE farm_id = :farm_id AND ended_at IS NULL
            ORDER BY created_at DESC
            LIMIT 1
            """
        )
        row = db.execute(q, {"farm_id": farm_id}).fetchone()
        if not row:
            return {
                "status": "success",
                "message": "No active farming session",
                "data": None,
            }
        return success_response(data=_row_to_dict(row))
    except Exception as e:
        logger.exception("get_session_by_farm_id failed: %s", e)
        raise error_response(message=f"Could not load farming session: {e!s}")


async def list_sessions_by_farmer(db: Session, farmer_id: str):
    try:
        q = text(
            """
            SELECT s.*, f.farm_name
            FROM farm_farming_session s
            JOIN farm f ON f.farm_id = s.farm_id
            WHERE s.farmer_id = :farmer_id
              AND s.ended_at IS NULL
            ORDER BY s.created_at DESC
            """
        )
        rows = db.execute(q, {"farmer_id": farmer_id}).fetchall()
        data = []
        for row in rows:
            d = _row_to_dict(row)
            if "farm_name" in row._mapping:
                d["farm_name"] = row._mapping["farm_name"]
            data.append(d)
        return success_response(data=data)
    except Exception as e:
        logger.exception("list_sessions_by_farmer failed: %s", e)
        raise error_response(message=f"Could not list farming sessions: {e!s}")


async def end_farming_session(db: Session, farm_id: str, farmer_id: str):
    """Mark the active session ended; row stays in DB for history."""
    try:
        if not _verify_farm_owner(db, farm_id, farmer_id):
            raise error_response(
                message="Farm not found or farmer_id does not own this farm.",
                status_code=403,
            )
        now = _as_utc(datetime.now(timezone.utc))
        result = db.execute(
            text(
                """
                UPDATE farm_farming_session
                SET ended_at = :ended_at
                WHERE farm_id = :farm_id
                  AND farmer_id = :farmer_id
                  AND ended_at IS NULL
                """
            ),
            {"farm_id": farm_id, "farmer_id": farmer_id, "ended_at": now},
        )
        db.commit()
        n = getattr(result, "rowcount", None)
        ended = bool(n and n > 0)
        return success_response(
            message="Farming session ended." if ended else "No active farming session for this farm.",
            data={"ended": ended, "removed": ended},
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.exception("end_farming_session failed: %s", e)
        raise error_response(message=f"Could not end farming session: {e!s}")
