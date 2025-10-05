"""Message endpoints for retrieving and managing email messages."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies.db import get_db
from app.api.v1.schemas.message import MessageResponse, MessageListResponse
from app.db.models.message import Message

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/", response_model=MessageListResponse)
async def list_messages(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    status: str = Query(None, description="Filter by analysis status"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all messages with pagination.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of messages per page (max 100)
    - **status**: Filter by analysis_status (pending, analyzing, completed, failed)
    """
    # Build query
    query = select(Message)
    
    # Apply filters
    if status:
        query = query.where(Message.analysis_status == status)
    
    # Get total count
    count_query = select(func.count()).select_from(Message)
    if status:
        count_query = count_query.where(Message.analysis_status == status)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Message.ingested_at.desc())
    
    # Execute query
    result = await db.execute(query)
    messages = result.scalars().all()
    
    # Calculate pages
    pages = (total + page_size - 1) // page_size
    
    return MessageListResponse(
        messages=messages,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific message by ID.
    
    - **message_id**: UUID of the message
    """
    result = await db.execute(
        select(Message).where(Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message
