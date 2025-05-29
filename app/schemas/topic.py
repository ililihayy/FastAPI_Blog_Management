from pydantic import BaseModel
from datetime import datetime


class TopicBase(BaseModel):
    name: str
    description: str


class TopicCreate(TopicBase): ...


class TopicUpdate(TopicBase): ...


class TopicInDB(TopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
