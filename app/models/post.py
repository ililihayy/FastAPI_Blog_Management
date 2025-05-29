from sqlalchemy import Integer, String, Text, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import func
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, nullable=False)
    content = mapped_column(Text, nullable=False)
    topic_id = mapped_column(Integer, ForeignKey("topics.id"))
    topic = relationship("Topic", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
