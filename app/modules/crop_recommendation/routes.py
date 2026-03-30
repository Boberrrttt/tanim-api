from fastapi import APIRouter

from ...docs.crop_recommendation_docs import (
    CREATE_CROP_RECOMMENDATION_DOCS,
    GET_CROP_RECOMMENDATIONS_BY_FARM_ID_DOCS,
    UPDATE_CROP_RECOMMENDATION_DOCS,
)
from .controllers import (
    create_crop_recommendation_controller,
    get_crop_recommendations_by_farm_id_controller,
    update_crop_recommendation_controller,
)

router = APIRouter(prefix="/crop-recommendations", tags=["Crop Recommendation"])

router.post("/", **CREATE_CROP_RECOMMENDATION_DOCS)(
    create_crop_recommendation_controller
)
router.put("/", **UPDATE_CROP_RECOMMENDATION_DOCS)(
    update_crop_recommendation_controller
)
router.get("/{farm_id}", **GET_CROP_RECOMMENDATIONS_BY_FARM_ID_DOCS)(
    get_crop_recommendations_by_farm_id_controller
)
