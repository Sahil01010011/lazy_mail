"""
Verdict model - stores final analysis decision and risk score.
"""
from sqlalchemy import Column, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Verdict(Base):
    """Analysis verdict with risk score and classification."""
    
    __tablename__ = "verdicts"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to message
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Classification
    classification = Column(String(50), nullable=False, index=True)  # phishing, spam, clean, suspicious, bec
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    risk_score = Column(Float, nullable=False, index=True)  # 0 to 100
    
    # Contributing factors
    rspamd_score = Column(Float, nullable=True)
    rspamd_action = Column(String(50), nullable=True)  # reject, rewrite subject, add header, no action
    rspamd_symbols = Column(JSON, nullable=True)  # List of triggered rules
    
    # Feature scores
    auth_score = Column(Float, nullable=True)
    url_score = Column(Float, nullable=True)
    content_score = Column(Float, nullable=True)
    stylometry_score = Column(Float, nullable=True)
    
    # Explanation
    explanation = Column(JSON, nullable=True)  # List of reasons for verdict
    threat_indicators = Column(JSON, nullable=True)  # Specific IOCs found
    
    # Actions taken
    action_taken = Column(String(50), nullable=True)  # quarantine, label, alert, none
    action_timestamp = Column(DateTime(timezone=True), nullable=True)
    
    # Analyst feedback
    analyst_label = Column(String(50), nullable=True)  # true_positive, false_positive, etc.
    analyst_notes = Column(Text, nullable=True)
    analyst_timestamp = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<Verdict {self.classification} ({self.risk_score:.1f}) for message {self.message_id}>"
