from sqlalchemy import Integer, String, Text
from ..database import Base
from sqlalchemy.orm import relationship, mapped_column


class Topic(Base):
    __tablename__ = "topics"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String, index=True, nullable=False)
    description = mapped_column(Text, index=True, nullable=False)
    post = relationship("Post", back_populates="topic", cascade="all, delete")
