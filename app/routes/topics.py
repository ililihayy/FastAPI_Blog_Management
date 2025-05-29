from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas import TopicCreate, TopicUpdate, TopicRead, PostCreate, PostRead
from ..database import get_db
from ..crud import create_topic, get_topics, get_topic, update_topic, delete_topic, create_post_with_topic


router = APIRouter(prefix="/topics", tags=["Topics"])


@router.post("/", response_model=TopicRead)
async def create_topic_route(topic: TopicCreate, db: AsyncSession = Depends(get_db)):
    return await create_topic(db, topic)


@router.get("/", response_model=List[TopicRead])
async def list_topics(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    return await get_topics(db, skip, limit)


@router.get("/{topic_id}", response_model=TopicRead)
async def get_topic_route(topic_id: int, db: AsyncSession = Depends(get_db)):
    topic = await get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/{topic_id}", response_model=TopicRead)
async def update_topic_route(topic_id: int, topic_data: TopicUpdate, db: AsyncSession = Depends(get_db)):
    topic = await update_topic(db, topic_id, topic_data)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.delete("/{topic_id}")
async def delete_topic_route(topic_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_topic(db, topic_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete topic with posts or topic not found")
    return {"detail": "Topic deleted successfully"}


@router.post("/{topic_id}/posts", response_model=PostRead)
async def create_post_for_topic(topic_id: int, post: PostCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_post_with_topic(db, post, topic_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
