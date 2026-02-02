from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import register_routes
import os
import joblib

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
    - **ML Predictions**: Crop recommendation system
    
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
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def optimize_model_if_needed():
    """Check if optimized model exists, create it if not"""
    try:
        model_path = os.path.join(os.path.dirname(__file__), "models", "tanim_model.pkl")
        optimized_path = os.path.join(os.path.dirname(__file__), "models", "tanim_model_optimized.pkl")
        
        if os.path.exists(optimized_path):
            print("✅ Optimized model already exists")
            return
        
        if not os.path.exists(model_path):
            print("❌ Original model not found")
            return
        
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"📊 Current model size: {size_mb:.2f} MB")
        
        if size_mb > 50:
            print("🔄 Optimizing model for deployment...")
            
            model = joblib.load(model_path)
            joblib.dump(model, optimized_path, compress=9)
            
            new_size_mb = os.path.getsize(optimized_path) / (1024 * 1024)
            reduction = ((size_mb - new_size_mb) / size_mb * 100)
            
            print(f"✅ Optimized model size: {new_size_mb:.2f} MB")
            print(f"📉 Size reduction: {reduction:.1f}%")
            
            if new_size_mb < size_mb:
                os.remove(model_path)
                print("🗑️  Removed original model (optimized version is smaller)")
        else:
            print("✅ Model size is acceptable, no optimization needed")
            
    except Exception as e:
        print(f"❌ Model optimization failed: {str(e)}")

@app.on_event("startup")
async def startup():
    print("🚀 Starting Tanim API...")
    
    optimize_model_if_needed()
    
    register_routes(app)
    
    print("✅ Tanim API is ready!")

@app.get("/")
async def root():
    return {"status": "success", "message": "Tanim API is running!"}
