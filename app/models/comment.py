from sqlalchemy import Integer, Text, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship, mapped_column


class Comment(Base):
    __tablename__ = "comments"

    id = mapped_column(Integer, primary_key=True, index=True)
    content = mapped_column(Text, nullable=False)
    post_id = mapped_column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")
