from fastapi import APIRouter, Query
from .controllers import get_today_weather_controller
from ...docs.weather_docs import GET_TODAY_WEATHER_DOCS

router = APIRouter(prefix="/weather", tags=["Weather"])

router.get("/", **GET_TODAY_WEATHER_DOCS)(get_today_weather_controller)
