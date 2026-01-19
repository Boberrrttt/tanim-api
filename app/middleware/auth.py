from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os

security = HTTPBearer()

class AuthMiddleware:
    def __init__(self, required_roles: Optional[list] = None):
        self.required_roles = required_roles or []
    
    async def __call__(self, request: Request):
        if self.should_skip_auth(request):
            return None
            
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token missing"
            )
        
        try:
            payload = verify_token(access_token)
            request.state.user = payload
            return payload
            
        except HTTPException:
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Both tokens invalid"
                )
            
            try:
                refresh_payload = verify_token(refresh_token)
                new_access_token = generate_access_token(refresh_payload)
                
                request.state.user = refresh_payload
                request.state.new_access_token = new_access_token
                
                return refresh_payload
                
            except HTTPException:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token invalid"
                )
    
    def should_skip_auth(self, request: Request) -> bool:
        skip_paths = [
            "/api/v1/auth/farmer",
            "/api/v1/auth/signup", 
            "/api/v1/auth/admin",
        ]
        return any(request.url.path.startswith(path) for path in skip_paths)