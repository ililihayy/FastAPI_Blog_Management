from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from ..models import Post, Comment
from ..schemas import PostCreate, PostUpdate
from typing import List, Optional
from sqlalchemy import asc, desc


async def create_post(db: AsyncSession, post: PostCreate) -> Post:
    db_post = Post(**post.model_dump())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def get_posts(
    db: AsyncSession, skip: int = 0, limit: int = 100, sort_by: str = "id", order: str = "asc"
) -> List[Post]:
    if not hasattr(Post, sort_by):
        sort_by = "id"

    order_func = asc if order.lower() == "asc" else desc

    sort_column = getattr(Post, sort_by)
    result = await db.execute(select(Post).order_by(order_func(sort_column)).offset(skip).limit(limit))
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: int) -> Optional[Post]:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def update_post(db: AsyncSession, post_id: int, post_data: PostUpdate) -> Optional[Post]:
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()

    if db_post is None:
        return None

    for key, value in post_data.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)

    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: int) -> bool:
    await db.execute(delete(Comment).where(Comment.post_id == post_id))
    result = await db.execute(delete(Post).where(Post.id == post_id).returning(Post.id))
    deleted_post_id = result.scalar_one_or_none()

    if deleted_post_id is None:
        await db.rollback()
        return False

    await db.commit()
    return True
