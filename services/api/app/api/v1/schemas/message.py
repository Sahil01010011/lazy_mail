"""Pydantic schemas for Message API responses."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """Base message fields."""
    message_id: str = Field(..., description="RFC 5322 Message-ID")
    account_id: str = Field(..., description="Email account identifier")
    subject: Optional[str] = Field(None, description="Email subject")
    sender: str = Field(..., description="Sender email address")
    recipients: Optional[List[str]] = Field(None, description="Recipient email addresses")


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None
    spf_result: Optional[str] = None
    dkim_result: Optional[str] = None
    dmarc_result: Optional[str] = None
    received_date: Optional[datetime] = None


class MessageResponse(MessageBase):
    """Schema for message API response."""
    id: UUID
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    has_attachments: bool = False
    attachment_count: int = 0
    spf_result: Optional[str] = None
    dkim_result: Optional[str] = None
    dmarc_result: Optional[str] = None
    analysis_status: str = "pending"
    ingested_at: datetime
    analyzed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)


class MessageListResponse(BaseModel):
    """Paginated list of messages."""
    messages: List[MessageResponse]
    total: int
    page: int
    page_size: int
    pages: int
