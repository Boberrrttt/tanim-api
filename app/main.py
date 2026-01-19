from fastapi import FastAPI
from .routes import register_routes

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

register_routes(app)  

