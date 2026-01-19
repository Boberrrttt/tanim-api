from dotenv import load_dotenv
import os
from datetime import timedelta
import re


load_dotenv()

DATABASE_URL = str(os.getenv("DATABASE_URL"))
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_REFRESH = os.getenv("JWT_REFRESH")
JWT_EXPIRES_IN = os.getenv("JWT_EXPIRES_IN", "1h")
JWT_REFRESH_EXPIRES_IN = os.getenv("JWT_REFRESH_EXPIRES_IN", "3d")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

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

ACCESS_TOKEN_TTL = parse_duration(JWT_EXPIRES_IN)
REFRESH_TOKEN_TTL = parse_duration(JWT_REFRESH_EXPIRES_IN)

