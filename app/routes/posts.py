from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas import PostCreate, PostUpdate, PostRead
from ..database import get_db
from ..crud import create_post, get_posts, get_post, update_post, delete_post

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostRead)
async def create_post_route(post: PostCreate, db: AsyncSession = Depends(get_db)):
    return await create_post(db, post)


@router.get("/", response_model=List[PostRead])
async def list_posts(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    sort_by: str = Query("id"),
    order: str = Query("asc", regex="^(asc|desc)$"),
):
    return await get_posts(db, skip=skip, limit=limit, sort_by=sort_by, order=order)


@router.get("/{post_id}", response_model=PostRead)
async def get_post_route(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await get_post(db, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostRead)
async def update_post_route(post_id: int, post_data: PostUpdate, db: AsyncSession = Depends(get_db)):
    post = await update_post(db, post_id, post_data)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
async def delete_post_route(post_id: int, db: AsyncSession = Depends(get_db)):
    success = await delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or not deleted")
    return {"detail": "Post deleted successfully"}
