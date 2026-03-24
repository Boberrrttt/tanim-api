from sqlalchemy.orm import Session
from .services import get_all
from ...core.database import get_db
from fastapi import Depends


async def get_all_farmers_controller(db: Session = Depends(get_db)):
    return await get_all(db)
