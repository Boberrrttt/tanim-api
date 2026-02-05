import os
import re
from datetime import timedelta
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

def parse_duration(value: str) -> timedelta:
    match = re.match(r"^(\d+)([smhd])$", value)
    if not match:
        raise ValueError(f"Invalid duration format: {value}")

    amount, unit = match.groups()
    amount = int(amount)

    return {
        "s": timedelta(seconds=amount),
        "m": timedelta(minutes=amount),
        "h": timedelta(hours=amount),
        "d": timedelta(days=amount),
    }[unit]

@lru_cache
def get_settings():
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_REFRESH = os.getenv("JWT_REFRESH")

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is missing")

    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is missing")

    jwt_expires_raw = os.getenv("JWT_EXPIRES_IN", "1h")
    jwt_refresh_raw = os.getenv("JWT_REFRESH_EXPIRES_IN", "3d")

    return {
        "DATABASE_URL": DATABASE_URL,
        "JWT_SECRET": JWT_SECRET,
        "JWT_REFRESH": JWT_REFRESH,
        "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
        "ACCESS_TOKEN_TTL": parse_duration(jwt_expires_raw),
        "REFRESH_TOKEN_TTL": parse_duration(jwt_refresh_raw),
    }
