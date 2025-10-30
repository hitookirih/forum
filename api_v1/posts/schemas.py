from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    body: str
    user_id: int


class PostCreate(BaseModel):
    pass

class Posts(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
