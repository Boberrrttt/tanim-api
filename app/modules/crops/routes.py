from fastapi import APIRouter

from .controllers import get_crop_timelines_controller
from ...docs.crops_docs import GET_CROP_TIMELINES_DOCS

router = APIRouter(prefix="/crops", tags=["Crops"])

router.get("/timeline", **GET_CROP_TIMELINES_DOCS)(get_crop_timelines_controller)
