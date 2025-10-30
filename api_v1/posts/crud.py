"""
CREATE
READ
UPDATE
DELETE
"""
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Post


async def get_posts(session: AsyncSession) -> list[Post]:
    stmt = select(Post).order_by(Post.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars().all()
    return list(posts)


async def get_post_by_id(session: AsyncSession, id: int) -> Post | None:
    return await session.get(Post, id)