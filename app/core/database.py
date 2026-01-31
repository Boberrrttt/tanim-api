from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings  

Base = declarative_base()

def get_engine():
    settings = get_settings()
    DATABASE_URL = settings["DATABASE_URL"]

    return create_engine(
        DATABASE_URL,
        connect_args={"sslmode": "require"},  
        pool_pre_ping=True,
        pool_recycle=300,
    )

def get_db():
    engine = get_engine()
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
