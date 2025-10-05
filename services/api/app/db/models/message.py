"""
Message model - stores raw email data and metadata.
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Message(Base):
    """Represents an email message with headers and content."""
    
    __tablename__ = "messages"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Email identifiers
    message_id = Column(String(500), unique=True, index=True, nullable=False)  # RFC 5322 Message-ID
    account_id = Column(String(255), index=True, nullable=False)  # Gmail/IMAP account
    
    # Email metadata
    subject = Column(Text, nullable=True)
    sender = Column(String(500), nullable=False, index=True)
    recipients = Column(JSON, nullable=True)  # List of recipient addresses
    cc = Column(JSON, nullable=True)
    bcc = Column(JSON, nullable=True)
    reply_to = Column(String(500), nullable=True)
    
    # Content
    body_text = Column(Text, nullable=True)  # Plain text version
    body_html = Column(Text, nullable=True)  # HTML version
    headers = Column(JSON, nullable=True)    # All email headers as JSON
    
    # Attachments
    has_attachments = Column(Boolean, default=False)
    attachment_count = Column(Integer, default=0)
    attachment_names = Column(JSON, nullable=True)  # List of filenames
    
    # Authentication results
    spf_result = Column(String(50), nullable=True)
    dkim_result = Column(String(50), nullable=True)
    dmarc_result = Column(String(50), nullable=True)
    
    # Timestamps
    received_date = Column(DateTime(timezone=True), nullable=True)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    analyzed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    analysis_status = Column(String(50), default="pending", index=True)  # pending, analyzing, completed, failed
    
    def __repr__(self):
        return f"<Message {self.message_id[:50]}... from {self.sender}>"
