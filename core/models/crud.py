import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from core.models import db_helper, User, Post


async def create_user(
        session: AsyncSession,
        nickname: str,
        email: EmailStr,
        name: str | None = None,
        fullname: str | None = None,
) -> User:
    user = User(
        nickname=nickname,
        name=name,
        fullname=fullname,
        email=email,
    )
    session.add(user)
    await session.commit()
    print(user)
    return user


async def create_posts(
        session: AsyncSession,
        user_id: int,
        *posts_title: str,
)-> list[Post]:
    posts = [
        Post(title=title, user_id=user_id)
        for title in posts_title
    ]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_user_by_nickname(session: AsyncSession, nickname: str) -> User | None:
    stmt = select(User).where(User.nickname == nickname)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print("found user", nickname,user)
    return user


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, nickname="horse",name="jack",fullname="bo",email='test@example.com')
        # await create_user(session=session, nickname="furry", email='test3@gmail.com')
        user_horse = await get_user_by_nickname(session=session, nickname="horse")
        user_anna = await get_user_by_nickname(session=session, nickname="anna")
        # await get_user_by_nickname(session=session, nickname="pork")
        # await create_posts(
        #     session,
        #     user_horse.id,
        #     "About weather",
        #     "Today is cold",
        # )
        # await create_posts(
        #     session,
        #     user_anna.id,
        #     "About music",
        # )


if __name__ == "__main__":
    asyncio.run(main())
