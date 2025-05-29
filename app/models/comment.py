from datetime import datetime
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy import func
from ..database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped


class Comment(Base):
    id = mapped_column(Integer, primary_key=True, index=True)
    content = mapped_column(Text, nullable=False)
    post_id = mapped_column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
