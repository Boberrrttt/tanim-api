from fastapi import APIRouter
from .controllers import get_all_farmers_controller
from ...docs.farmer_docs import GET_ALL_FARMERS_DOCS

router = APIRouter(prefix="/farmers", tags=["Farmer"])

router.get("/", **GET_ALL_FARMERS_DOCS)(get_all_farmers_controller)

