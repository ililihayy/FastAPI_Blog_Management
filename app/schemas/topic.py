from pydantic import BaseModel


class TopicBase(BaseModel):
    name: str
    description: str


class TopicCreate(TopicBase): ...


class TopicUpdate(TopicBase): ...


class TopicInDB(TopicBase):
    id: int

    class Config:
        orm_mode = True


class TopicRead(TopicInDB): ...
