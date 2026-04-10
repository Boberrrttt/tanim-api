from fastapi import APIRouter

from .controllers import (
    delete_farming_session_controller,
    get_farming_session_by_farm_controller,
    list_farming_sessions_by_farmer_controller,
    start_farming_session_controller,
)

router = APIRouter(prefix="/farm/farming", tags=["Farm farming session"])

router.post(
    "/start",
    summary="Pin farm: save soil, crop, and fertilizer snapshot (stops using ML pending slot for this farm)",
)(start_farming_session_controller)

router.get(
    "/by-farmer/{farmer_id}",
    summary="List farming sessions for banner and hydration",
)(list_farming_sessions_by_farmer_controller)

router.get(
    "/{farm_id}",
    summary="Get farming session for one farm",
)(get_farming_session_by_farm_controller)

router.delete(
    "/{farm_id}",
    summary="End farming: mark session ended (row kept); same farmer must own the farm",
)(delete_farming_session_controller)
