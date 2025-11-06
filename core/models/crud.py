import asyncio
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from sqlalchemy.orm import joinedload, selectinload
from auth import utils as auth_utils

from core.models import db_helper, User, Post
from core.models.user_schemas import UserUpdateSchema


async def create_user(
        session: AsyncSession,
        nickname: str,
        email: EmailStr,
        password: str,
        name: str | None = None,
        fullname: str | None = None,
) -> User:
    user = User(
        nickname=nickname,
        name=name,
        fullname=fullname,
        email=email,
        password=password,
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


async def update_user_partial(
        session: AsyncSession,
        user: User,
        user_update: UserUpdateSchema,
)-> User:
    # data = user_update.model_dump(exclude_unset=True)
    #
    # if "password" in data:
    #     data["password"] = auth_utils.hash_password(data["password"])

    for column, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, column, value)
    await session.commit()
    await session.refresh(user)
    print(user)
    return user


async def get_user_by_nickname(session: AsyncSession, nickname: str) -> User | None:
    stmt = select(User).where(User.nickname == nickname)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    print("found user", nickname,user)
    return user


async def get_user_with_posts(
        session: AsyncSession,
):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars()

    for user in users:
        print("^^" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, nickname="horse",name="jack",fullname="bo",email='test@example.com')
        # await create_user(session=session, nickname="John", email="johnnn@mail.com", password=auth_utils.hash_password("password"))
        # await get_user_by_nickname(session=session, nickname="john", )
        # user_anna = await get_user_by_nickname(session=session, nickname="anna")
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
        # await update_user_partial(session=session, user=user_anna, user_update=UserUpdateSchema(name='David', fullname="jones"))
        await get_user_with_posts(session=session)


if __name__ == "__main__":
    asyncio.run(main())
