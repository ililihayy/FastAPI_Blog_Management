from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas import CommentCreate, CommentUpdate, CommentRead
from ..database import get_db
from ..crud import (
    create_comment,
    get_comments_for_post,
    get_comment,
    update_comment,
    delete_comment,
)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/post/{post_id}", response_model=CommentRead, description="Create a new comment for a specific post")
async def create_comment_route(post_id: int, comment: CommentCreate, db: AsyncSession = Depends(get_db)) -> CommentRead:
    return await create_comment(db, comment, post_id)


@router.get(
    "/post/{post_id}",
    response_model=List[CommentRead],
    description="List comments for a specific post with pagination and sorting",
)
async def list_comments_for_post(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    db: AsyncSession = Depends(get_db),
) -> List[CommentRead]:
    comments = await get_comments_for_post(db, post_id, skip=skip, limit=limit, sort_by=sort_by, order=order)
    return comments  # type: ignore[return-value]


@router.get("/{comment_id}", response_model=CommentRead, description="Get a single comment by its ID")
async def get_comment_route(comment_id: int, db: AsyncSession = Depends(get_db)) -> CommentRead:
    comment = await get_comment(db, comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=CommentRead, description="Update a comment by its ID")
async def update_comment_route(
    comment_id: int, comment_data: CommentUpdate, db: AsyncSession = Depends(get_db)
) -> CommentRead:
    comment = await update_comment(db, comment_id, comment_data)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.delete("/{comment_id}", description="Delete a comment by its ID")
async def delete_comment_route(comment_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    success = await delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found or not deleted")
    return {"detail": "Comment deleted successfully"}
