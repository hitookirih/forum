from typing import TYPE_CHECKING
from typing import Optional, List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from core.models.base import Base


if TYPE_CHECKING:
    from .post import Post

class User(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String(34), nullable=False, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(34))
    fullname: Mapped[Optional[str]]

    addresses: Mapped['Email'] = relationship(back_populates="users",)

    posts: Mapped[list['Post']] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f'<User {self.id!r}, nickname: {self.nickname!r}, fullname: {self.fullname!r}, name: {self.name!r}>'

class Email(Base):
    __tablename__ = 'email_addresses'

    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped["User"] = relationship(back_populates='email_addresses')

    def __repr__(self) -> str:
        return f'Email(id={self.id!r}, email_address={self.email_address!r})'