from fastapi import APIRouter
from .controllers import create_soil_health_test_controller, get_soil_health_tests_by_farm_id_controller
from ...docs.soil_health_test_docs import CREATE_SOIL_HEALTH_TEST_DOCS, GET_SOIL_HEALTH_TESTS_BY_FARM_ID_DOCS

router = APIRouter(prefix="/test", tags=["Soil Health Test"])

router.post("/", **CREATE_SOIL_HEALTH_TEST_DOCS)(create_soil_health_test_controller)
router.get("/{farm_id}", **GET_SOIL_HEALTH_TESTS_BY_FARM_ID_DOCS)(get_soil_health_tests_by_farm_id_controller)
