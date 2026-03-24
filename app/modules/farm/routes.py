from fastapi import APIRouter
from .controllers import create_farm_controller, get_all_farms_controller, get_farms_by_farmer_id_controller
from ...docs.farm_docs import CREATE_FARM_DOCS, GET_ALL_FARMS_DOCS, GET_FARMS_BY_FARMER_ID_DOCS

router = APIRouter(prefix="/farm", tags=["Farm"])

router.post("/", **CREATE_FARM_DOCS)(create_farm_controller)
router.get("/", **GET_ALL_FARMS_DOCS)(get_all_farms_controller)
router.get("/{farmer_id}", **GET_FARMS_BY_FARMER_ID_DOCS)(get_farms_by_farmer_id_controller)
