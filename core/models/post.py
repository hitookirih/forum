from typing import TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User

class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="posts")

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, title: {self.title!r}, user_id: {self.user_id!r})'

    def __repr__(self) -> str:
        return str(self)
