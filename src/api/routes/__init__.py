from fastapi import APIRouter

from .redirects import router as redirects_router

api_router = APIRouter()
api_router.include_router(redirects_router)