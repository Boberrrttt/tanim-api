from fastapi import APIRouter

from ...docs.ml_docs import (
    FERTILIZER_PREDICT_DOCS,
    GET_MODEL_INFO_DOCS,
    PREDICT_DOCS,
)
from .controllers import (
    delete_pending_soil_controller,
    get_model_info_controller,
    get_pending_soil_controller,
    predict_controller,
    predict_fertilizer_controller,
)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

router.post("/", **PREDICT_DOCS)(predict_controller)
router.post("/fertilizer", **FERTILIZER_PREDICT_DOCS)(predict_fertilizer_controller)
router.get("/", **GET_MODEL_INFO_DOCS)(get_model_info_controller)
router.get(
    "/pending-soil",
    summary="Proxy: ML pending soil cache",
    description="Forwards to the inference service GET /pending/soil when the app shares one public URL with tanim-api.",
)(get_pending_soil_controller)
router.delete(
    "/pending-soil",
    summary="Proxy: clear ML pending soil cache",
)(delete_pending_soil_controller)
