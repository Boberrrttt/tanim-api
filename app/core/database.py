from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings

Base = declarative_base()

# One Engine + SessionLocal per process (Vercel/Lambda: one per warm instance).
# Creating a new Engine on every request multiplied pools and exhausted Supabase
# Session pooler (MaxClientsInSessionMode). Use Transaction pooler :6543 in prod.
_engine = None
_SessionLocal = None


def _ensure_engine():
    global _engine, _SessionLocal
    if _engine is not None:
        return
    settings = get_settings()
    DATABASE_URL = settings["DATABASE_URL"]
    _engine = create_engine(
        DATABASE_URL,
        connect_args={
            "sslmode": "require",
            # PgBouncer transaction mode (port 6543): disable server-side prepare
            "prepare_threshold": None,
        },
        pool_pre_ping=True,
        pool_recycle=300,
        # Serverless: keep concurrent DB sessions per instance minimal
        pool_size=1,
        max_overflow=0,
    )
    _SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_engine,
    )


def get_engine():
    _ensure_engine()
    return _engine


def get_db():
    _ensure_engine()
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
