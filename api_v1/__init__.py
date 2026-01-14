from fastapi import APIRouter

from .posts.views import router as posts_router
from api_v1.auth.views import router as auth_router

router = APIRouter()
router.include_router(router=posts_router, prefix="/posts")

router.include_router(router=auth_router)