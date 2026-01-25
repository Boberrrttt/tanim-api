from fastapi import APIRouter
from .controllers import create_farm_controller
from ...docs.farm_docs import CREATE_FARM_DOCS, create_farm_example

router = APIRouter(prefix="/farm", tags=["Farm"])

router.post("/", **CREATE_FARM_DOCS)(create_farm_controller)