from fastapi import Request, Response
from .auth import AuthMiddleware

def require_auth():
    async def dependency(request: Request, response: Response = None):
        auth_middleware = AuthMiddleware()
        user = await auth_middleware(request)
        
        if response and hasattr(request.state, 'access_token'):
            response.set_cookie(
                key="access_token",
                value=request.state.access_token,
                httponly=True,
                secure=True,
                samesite="none",
                max_age=1 * 24 * 60 * 60
            )
        
        return user
    return dependency
