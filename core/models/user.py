from typing import TYPE_CHECKING
from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.models.base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    __tablename__ = "users"
    # __table_args__ = {'extend_existing': True}

    nickname: Mapped[str] = mapped_column(String(34), nullable=False, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(34))
    fullname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String,nullable=False, unique=True)
    posts: Mapped[list['Post']] = relationship(back_populates="user")


    def __repr__(self) -> str:
        return f'<User {self.id!r}, nickname: {self.nickname!r}, fullname: {self.fullname!r}, name: {self.name!r}>'


    def __str__(self) -> str:
        return f'Nickname: {self.nickname!r}, Email: {self.email!r}'
