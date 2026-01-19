from .modules.auth.routes import router as auth_router

def register_routes(app):
    app.include_router(auth_router, prefix="/api/v1")
