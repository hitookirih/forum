import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from core.models import db_helper, User, Post


async def create_user(
        session: AsyncSession,
        nickname: str,
        name: str,
        fullname: str,
        email: EmailStr,
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


async def main():
    async with db_helper.session_factory() as session:
        await create_user(session=session, nickname="horse",name="jack",fullname="bo",email='test@example.com')
        # await create_user(session=session, nickname="anna", email='testtwo@gmail.com')


if __name__ == "__main__":
    asyncio.run(main())
