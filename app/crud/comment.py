from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, asc, desc

from ..models import Comment
from ..schemas import CommentCreate, CommentUpdate


async def create_comment(db: AsyncSession, comment: CommentCreate, post_id: int) -> Comment:
    db_comment = Comment(**comment.model_dump())
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comments_for_post(
    db: AsyncSession, post_id: int, skip: int = 0, limit: int = 100, sort_by: str = "id", order: str = "asc"
) -> List[Comment]:
    if not hasattr(Comment, sort_by):
        sort_by = "id"

    order_func = asc if order.lower() == "asc" else desc
    sort_column = getattr(Comment, sort_by)

    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id).order_by(order_func(sort_column)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_comment(db: AsyncSession, comment_id: int) -> Optional[Comment]:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalar_one_or_none()


async def update_comment(db: AsyncSession, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    db_comment = result.scalar_one_or_none()

    if not db_comment:
        return None

    for key, value in comment_data.model_dump(exclude_unset=True).items():
        setattr(db_comment, key, value)

    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    result = await db.execute(delete(Comment).where(Comment.id == comment_id).returning(Comment.id))
    deleted_comment_id = result.scalar_one_or_none()

    if deleted_comment_id is None:
        await db.rollback()
        return False

    await db.commit()
    return True
