from sqlalchemy.orm import Session
from .services import get_today_weather
from fastapi import Query

async def get_today_weather_controller(
    lat: float = Query(..., description="Latitude of the location"),
    lon: float = Query(..., description="Longitude of the location")
):
    return await get_today_weather(lat, lon)
