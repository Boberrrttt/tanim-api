from fastapi import APIRouter
from .controllers import login_farmer_controller, signup_admin_controller, signup_farmer_controller, login_admin_controller
from ...docs.auth_docs import (
    ADMIN_SIGNUP_DOCS,
    FARMER_LOGIN_DOCS, 
    FARMER_SIGNUP_DOCS, 
    ADMIN_LOGIN_DOCS
)

router = APIRouter(prefix="/auth", tags=["Auth"])

router.post("/login-farmer", **FARMER_LOGIN_DOCS)(login_farmer_controller)
router.post("/signup-farmer", **FARMER_SIGNUP_DOCS)(signup_farmer_controller)
router.post("/login-admin", **ADMIN_LOGIN_DOCS)(login_admin_controller)
router.post("/signup-admin", **ADMIN_SIGNUP_DOCS)(signup_admin_controller)
