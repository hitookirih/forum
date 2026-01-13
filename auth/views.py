from fastapi import APIRouter

from .jwt_auth import router as jwt_router

router = APIRouter()
router.include_router(router=jwt_router)

