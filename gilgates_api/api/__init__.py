from fastapi import APIRouter
from .login import router as login_router
from .signup import router as signup_router
from .user import router as user_router
from .employee import router as employee_router

api_router = APIRouter()
api_router.include_router(login_router, tags=["auth"])
api_router.include_router(signup_router, tags=["auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(employee_router, prefix="/employee", tags=["employee"])
