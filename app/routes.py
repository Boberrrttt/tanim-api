from .modules.auth.routes import router as auth_router
from .modules.farm.routes import router as farm_router

prefix = '/api/v1'

def register_routes(app):
    app.include_router(auth_router, prefix=prefix)
    app.include_router(farm_router, prefix=prefix)