from fastapi import APIRouter

from ...docs.soil_health_test_docs import (
    CREATE_SOIL_HEALTH_TEST_DOCS,
    GET_SOIL_HEALTH_TESTS_BY_FARM_ID_DOCS,
    UPDATE_SOIL_HEALTH_TEST_DOCS,
    UPSERT_TODAY_SOIL_HEALTH_TEST_DOCS,
)
from .controllers import (
    create_soil_health_test_controller,
    get_soil_health_tests_by_farm_id_controller,
    update_soil_health_test_controller,
    upsert_soil_health_today_controller,
)

router = APIRouter(prefix="/test", tags=["Soil Health Test"])

router.post("/", **CREATE_SOIL_HEALTH_TEST_DOCS)(create_soil_health_test_controller)
router.put("/", **UPDATE_SOIL_HEALTH_TEST_DOCS)(update_soil_health_test_controller)
router.put("/upsert", **UPSERT_TODAY_SOIL_HEALTH_TEST_DOCS)(upsert_soil_health_today_controller)
router.get("/{farm_id}", **GET_SOIL_HEALTH_TESTS_BY_FARM_ID_DOCS)(get_soil_health_tests_by_farm_id_controller)
