from .modules.auth.routes import router as auth_router
from .modules.farm.routes import router as farm_router
from .modules.soil_health_test.routes import router as soil_health_test_router
from .modules.weather.routes import router as weather_router

prefix = '/api/v1'

def register_routes(app):
    app.include_router(auth_router, prefix=prefix)
    app.include_router(farm_router, prefix=prefix)
    app.include_router(soil_health_test_router, prefix=prefix)
    app.include_router(weather_router, prefix=prefix)