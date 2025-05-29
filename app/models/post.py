from sqlalchemy import Integer, String, Text, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship, mapped_column


class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String, nullable=False)
    content = mapped_column(Text, nullable=False)
    topic_id = mapped_column(Integer, ForeignKey("topics.id"))
    topic = relationship("Topic", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
