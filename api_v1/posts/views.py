from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .schemas import Posts, PostCreate

router = APIRouter(tags=["posts"])


@router.get("/", response_model=list[Posts])
async def get_posts(session: AsyncSession = Depends(db_helper.session_dependency)):
    return await crud.get_posts(session=session)


@router.get("/{post_id}", response_model=Posts)
async def get_post(id: int, session: AsyncSession = Depends(db_helper.session_dependency)):
    post = await crud.get_post_by_id(session=session, id=id)
    if post is not None:
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post {id} not found!"
    )
