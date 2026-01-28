from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Lazy import helper for routes
def lazy_register_routes(app):
    """
    Import routes only when serverless starts handling requests.
    Prevents import-time crashes on Vercel.
    """
    from app.routes import register_routes as rr
    rr(app)

# FastAPI app definition
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

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route for health check
@app.get("/")
def root():
    return {"status": "ok"}

lazy_register_routes(app)

handler = app
