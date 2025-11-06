from pydantic import BaseModel, EmailStr, ConfigDict


class UserBaseSchema(BaseModel):
    id: int


# class UserSchema(BaseModel):
#     model_config = ConfigDict
#
#     nickname: str
#     email: EmailStr
#     password: bytes
#     active: bool = True


class UserUpdateSchema(BaseModel):

    nickname: str | None = None
    name: str | None = None
    fullname: str | None = None
    email: EmailStr | None = None
    password: bytes | None = None


