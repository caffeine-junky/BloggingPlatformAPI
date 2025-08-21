from fastapi import APIRouter
from .post import router as posts_router

router = APIRouter(prefix="/v1")

router.include_router(posts_router)
