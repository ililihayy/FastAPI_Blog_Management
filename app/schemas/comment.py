from pydantic import BaseModel
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    post_id: int


class CommentCreate(CommentBase): ...


class CommentUpdate(CommentBase): ...


class CommentRead(CommentBase): ...


class CommentInDB(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
