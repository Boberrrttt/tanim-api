import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import register_routes

# Browsers reject Access-Control-Allow-Origin: * together with credentialed fetches.
# Starlette only mirrors a concrete Origin when allow_origins is not "*".
_DEFAULT_CORS_ORIGINS = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://localhost:8082",
    "http://127.0.0.1:8082",
    "http://localhost:19000",
    "http://127.0.0.1:19000",
    "http://localhost:19006",
    "http://127.0.0.1:19006",
]

# Optional comma-separated list, e.g. CORS_ORIGINS=https://app.example.com,http://localhost:3000
def _cors_allow_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "").strip()
    if raw:
        return [o.strip() for o in raw.split(",") if o.strip()]
    return list(_DEFAULT_CORS_ORIGINS)


# Expo (LAN / tunnel) and typical private-network dev hosts when Origin is sent.
_CORS_ORIGIN_REGEX = (
    r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"
    r"|^https?://192\.168\.\d{1,3}\.\d{1,3}(:\d+)?$"
    r"|^https?://10\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$"
    r"|^https://[\w.-]+\.exp\.direct(:\d+)?$"
)

app = FastAPI(
    title="Tanim API",
    description="""
    ## Tanim Agricultural Management API
    
    A comprehensive FastAPI backend for agricultural management with Supabase/Postgres integration.
    
    ### Features
    - **Authentication**: JWT-based auth with refresh tokens
    - **User Management**: Farmer and admin roles
    - **Security**: Cookie-based token management
    - **Database**: PostgreSQL with Supabase
    
    ### Authentication Flow
    1. Login with `/api/v1/auth/farmer` or `/api/v1/auth/admin`
    2. Receive access and refresh tokens in HTTP-only cookies
    3. Access protected routes automatically
    4. Tokens refresh automatically when expired
    
    ### Error Handling
    All responses follow a consistent format:
    - **Success**: `{"status": "success", "message": "...", "data": {...}}`
    - **Error**: `{"status": "error", "message": "...", "details": {...}}`
    
    ### Rate Limiting
    - Login attempts: 5 per minute
    - API calls: 100 per minute per user
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Tanim Support",
        "email": "support@tanim.com"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allow_origins(),
    allow_origin_regex=_CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register at import time so routes exist on serverless (Vercel) even when lifespan
# ordering differs; @app.on_event("startup") left only / and docs until startup ran.
register_routes(app)


@app.get("/")
async def root():
    return {"status": "success", "message": "Tanim API is running!"}
