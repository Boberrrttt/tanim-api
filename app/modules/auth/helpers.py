from typing import Dict, Optional
from datetime import datetime
from jose import jwt, JWTError
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ...core.config import (
    JWT_SECRET,
    JWT_REFRESH,
    JWT_ALGORITHM,
    ACCESS_TOKEN_TTL,
    REFRESH_TOKEN_TTL,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    truncated_password = password_bytes.decode("utf-8", errors="ignore")
    return pwd_context.hash(truncated_password)
    
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def generate_access_token(payload: dict) -> str:
    if JWT_SECRET is None:
        raise ValueError("secret not set")

    to_encode = payload.copy()
    to_encode.update({
        "exp": datetime.utcnow() + ACCESS_TOKEN_TTL,
        "type": "access"
    })

    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_refresh_token(payload: dict) -> str:
    if JWT_REFRESH is None:
        raise ValueError("refresh not set")

    to_encode = payload.copy()
    to_encode.update({
        "exp": datetime.utcnow() + REFRESH_TOKEN_TTL,
        "type": "refresh"
    })

    return jwt.encode(to_encode, JWT_REFRESH, algorithm=JWT_ALGORITHM)

def verify_access_token(token: str) -> Dict:
    try:
        if JWT_SECRET is None:
            raise ValueError("secret not set")

        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired or invalid"
        )


def verify_refresh_token(token: str) -> Optional[Dict]:
    try:
        if JWT_REFRESH is None:
            raise ValueError("refresh not set")

        payload = jwt.decode(token, JWT_REFRESH, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError as e:
        print("Refresh token verification failed:", str(e))
        return None
