from fastapi import APIRouter

from ...docs.ml_docs import (
    FERTILIZER_PREDICT_DOCS,
    GET_MODEL_INFO_DOCS,
    PREDICT_DOCS,
)
from .controllers import (
    get_model_info_controller,
    predict_controller,
    predict_fertilizer_controller,
)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

router.post("/", **PREDICT_DOCS)(predict_controller)
router.post("/fertilizer", **FERTILIZER_PREDICT_DOCS)(predict_fertilizer_controller)
router.get("/", **GET_MODEL_INFO_DOCS)(get_model_info_controller)
