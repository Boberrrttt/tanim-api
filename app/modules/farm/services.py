import logging
import json
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.modules.farm.schemas import CreateFarm
from app.modules.farm.models import Farm
from ...helpers.responses import success_response, error_response

logger = logging.getLogger(__name__)


def _farm_location_from_db(raw) -> Optional[str]:
    """Normalize DB value: plain address string, or legacy JSON with an `address` field."""
    if raw is None:
        return None
    text = raw.strip() if isinstance(raw, str) else str(raw).strip()
    if not text:
        return None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return text
    if isinstance(parsed, dict):
        addr = parsed.get("address")
        if addr is not None and str(addr).strip():
            return str(addr).strip()
        return None
    if isinstance(parsed, str) and parsed.strip():
        return parsed.strip()
    return None


def _float_or_none(val) -> Optional[float]:
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _legacy_lat_lng_from_raw(raw) -> tuple[Optional[float], Optional[float]]:
    """If farm_location still holds legacy JSON with coordinates, extract them."""
    if raw is None:
        return None, None
    text = raw.strip() if isinstance(raw, str) else str(raw).strip()
    if not text or not text.startswith("{"):
        return None, None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None, None
    if not isinstance(parsed, dict):
        return None, None
    lat = _float_or_none(parsed.get("latitude", parsed.get("lat")))
    lng = _float_or_none(parsed.get("longitude", parsed.get("lng")))
    return lat, lng


def _lat_lng_from_row(row) -> tuple[Optional[float], Optional[float]]:
    lat = _float_or_none(getattr(row, "latitude", None))
    lng = _float_or_none(getattr(row, "longitude", None))
    if lat is not None and lng is not None:
        return lat, lng
    return _legacy_lat_lng_from_raw(getattr(row, "farm_location", None))


async def create(db: Session, payload: CreateFarm):
    try:
        logger.info(
            "Farm creation attempt: farm_name=%r, farmer_id=%r",
            payload.farm_name,
            payload.farmer_id,
        )
        loc = None
        if payload.farm_location:
            s = payload.farm_location.strip()
            loc = s or None
        farm = Farm(
            farm_name=payload.farm_name,
            farm_measurement=payload.farm_measurement,
            farm_location=loc,
            latitude=payload.latitude,
            longitude=payload.longitude,
            farmer_id=payload.farmer_id
        )

        query = text("""
            INSERT INTO farm (
                farm_id, farm_name, farmer_id, farm_measurement, farm_location,
                latitude, longitude, created_at
            )
            VALUES (
                :farm_id, :farm_name, :farmer_id, :farm_measurement, :farm_location,
                :latitude, :longitude, :created_at
            )
        """)
        db.execute(query, {
            'farm_id': farm.farm_id,
            'farm_name': farm.farm_name,
            'farmer_id': payload.farmer_id,
            'farm_measurement': farm.farm_measurement,
            'farm_location': farm.farm_location,
            'latitude': farm.latitude,
            'longitude': farm.longitude,
            'created_at': farm.created_at.isoformat()
        })

        db.commit()
        
        return success_response(
            message="Farm created successfully",
            data=farm.to_dict()
        )
    
    except Exception as e:
        db.rollback()
        logger.exception(
            "Farm creation failed for farm_name=%r, farmer_id=%r: %s",
            payload.farm_name,
            payload.farmer_id,
            e,
        )
        return error_response(
            message="Farm creation failed"
        )


async def get_all(db: Session):
    try:
        query = text("""
            SELECT * FROM farm
        """)
        
        result = db.execute(query)

        if result.rowcount == 0:
            return success_response(
                message="No farms found",
                data=[],
                total=0
            )
        
        farms = []
        for row in result:
            farm_location = _farm_location_from_db(row.farm_location)
            lat, lng = _lat_lng_from_row(row)

            farmer_id = getattr(row, "farmer_id", None)
            farm = Farm(
                farm_id=row.farm_id,
                farm_name=row.farm_name,
                farm_measurement=row.farm_measurement,
                farm_location=farm_location,
                latitude=lat,
                longitude=lng,
                farmer_id=str(farmer_id) if farmer_id else None,
                created_at=row.created_at
            )
            farms.append(farm.to_dict())
        
        return success_response(
            message="Farms retrieved successfully",
            data=farms,
            total=len(farms)
        )
    
    except Exception:
        return error_response(
            message="Farm retrieval failed"
        )


async def get_by_farmer_id(db: Session, farmer_id: str):
    try:
        query = text("""
            SELECT * FROM farm
            WHERE farmer_id = :farmer_id
        """)
        result = db.execute(query, {"farmer_id": farmer_id})

        farms = []
        for row in result:
            farm_location = _farm_location_from_db(row.farm_location)
            lat, lng = _lat_lng_from_row(row)

            farmer_id_val = getattr(row, "farmer_id", None)
            farm = Farm(
                farm_id=row.farm_id,
                farm_name=row.farm_name,
                farm_measurement=row.farm_measurement,
                farm_location=farm_location,
                latitude=lat,
                longitude=lng,
                farmer_id=str(farmer_id_val) if farmer_id_val else None,
                created_at=row.created_at
            )
            farms.append(farm.to_dict())

        return success_response(
            message="Farms retrieved successfully",
            data=farms,
            total=len(farms)
        )

    except Exception:
        return error_response(
            message="Farm retrieval failed"
        )