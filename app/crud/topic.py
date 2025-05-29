from ..models import Topic, Post
from ..schemas import TopicCreate, TopicUpdate, PostCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, asc, desc
from typing import List, Optional


async def create_topic(db: AsyncSession, topic: TopicCreate) -> Topic:
    db_topic = Topic(**topic.model_dump())
    db.add(db_topic)
    await db.commit()
    await db.refresh(db_topic)
    return db_topic


async def get_topics(
    db: AsyncSession, skip: int = 0, limit: int = 100, sort_by: str = "id", order: str = "asc"
) -> List[Topic]:
    if not hasattr(Topic, sort_by):
        sort_by = "id"

    order_func = asc if order.lower() == "asc" else desc
    sort_column = getattr(Topic, sort_by)

    result = await db.execute(select(Topic).order_by(order_func(sort_column)).offset(skip).limit(limit))
    return result.scalars().all()


async def get_topic(db: AsyncSession, topic_id: int) -> Optional[Topic]:
    result = await db.execute(select(Topic).where(Topic.id == topic_id))
    return result.scalar_one_or_none()


async def update_topic(db: AsyncSession, topic_id: int, topic_data: TopicUpdate) -> Optional[Topic]:
    result = await db.execute(select(Topic).where(Topic.id == topic_id))
    db_topic = result.scalar_one_or_none()

    if db_topic is None:
        return None

    for key, value in topic_data.model_dump(exclude_unset=True).items():
        setattr(db_topic, key, value)

    await db.commit()
    await db.refresh(db_topic)
    return db_topic


async def delete_topic(db: AsyncSession, topic_id: int) -> bool:
    posts_exist = await db.execute(select(Post).where(Post.topic_id == topic_id).limit(1))
    if posts_exist.scalar_one_or_none() is not None:
        return False

    result = await db.execute(delete(Topic).where(Topic.id == topic_id).returning(Topic.id))
    deleted_topic_id = result.scalar_one_or_none()

    if deleted_topic_id is None:
        await db.rollback()
        return False

    await db.commit()
    return True


async def create_post_with_topic(db: AsyncSession, post: PostCreate, topic_id: int) -> Post:
    topic = await get_topic(db, topic_id)
    if topic is None:
        raise ValueError(f"Topic with ID {topic_id} does not exist")

    db_post = Post(**post.model_dump(), topic_id=topic_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post
