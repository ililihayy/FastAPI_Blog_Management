from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    topic_id: int


class PostCreate(PostBase): ...


class PostUpdate(PostBase): ...


class PostInDB(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostRead(PostInDB): ...
