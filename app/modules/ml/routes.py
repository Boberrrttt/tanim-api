from fastapi import APIRouter
from .controllers import predict_controller, get_model_info_controller
from ...docs.ml_docs import PREDICT_DOCS, GET_MODEL_INFO_DOCS

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# router.post("/", **PREDICT_DOCS)(predict_controller)
# router.get("/", **GET_MODEL_INFO_DOCS)(get_model_info_controller)
