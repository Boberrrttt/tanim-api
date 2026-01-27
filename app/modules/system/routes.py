from fastapi import APIRouter
from .controllers import create_system_controller, update_battery_status_controller
from ...docs.system_docs import CREATE_SYSTEM_DOCS, UPDATE_BATTERY_STATUS_DOCS

router = APIRouter(prefix="/system", tags=["System"])

router.post("/", **CREATE_SYSTEM_DOCS)(create_system_controller)
router.put("/", **UPDATE_BATTERY_STATUS_DOCS)(update_battery_status_controller)