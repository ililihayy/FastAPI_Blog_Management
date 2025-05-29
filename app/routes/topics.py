from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas import TopicCreate, TopicUpdate, TopicRead, PostCreate, PostRead
from ..database import get_db
from ..crud import create_topic, get_topics, get_topic, update_topic, delete_topic, create_post_with_topic


router = APIRouter(prefix="/topics", tags=["Topics"])


@router.post("/", response_model=TopicRead, description="Create a new topic")
async def create_topic_route(topic: TopicCreate, db: AsyncSession = Depends(get_db)) -> TopicRead:
    return await create_topic(db, topic)


@router.get("/", response_model=List[TopicRead], description="Retrieve a list of topics with pagination support")
async def list_topics(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100) -> List[TopicRead]:
    return await get_topics(db, skip, limit)  # type: ignore[return-value]


@router.get("/{topic_id}", response_model=TopicRead, description="Get a single topic by its ID")
async def get_topic_route(topic_id: int, db: AsyncSession = Depends(get_db)) -> TopicRead:
    topic = await get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/{topic_id}", response_model=TopicRead, description="Update a topic by its ID")
async def update_topic_route(topic_id: int, topic_data: TopicUpdate, db: AsyncSession = Depends(get_db)) -> TopicRead:
    topic = await update_topic(db, topic_id, topic_data)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.delete(
    "/{topic_id}", description="Delete a topic by its ID. Fails if topic has associated posts or does not exist."
)
async def delete_topic_route(topic_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    success = await delete_topic(db, topic_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete topic with posts or topic not found")
    return {"detail": "Topic deleted successfully"}


@router.post("/{topic_id}/posts", response_model=PostRead, description="Create a new post under a specific topic")
async def create_post_for_topic(topic_id: int, post: PostCreate, db: AsyncSession = Depends(get_db)) -> PostRead:
    try:
        return await create_post_with_topic(db, post, topic_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
