"""
Feature model - stores extracted features for ML and analysis.
"""
from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Feature(Base):
    """Extracted features from email content and metadata."""
    
    __tablename__ = "features"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key to message
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # URL features
    url_count = Column(Integer, default=0)
    unique_domains = Column(Integer, default=0)
    suspicious_tlds = Column(Integer, default=0)
    url_shorteners = Column(Integer, default=0)
    homograph_count = Column(Integer, default=0)
    extracted_urls = Column(JSON, nullable=True)  # List of all URLs
    
    # Content features
    body_length = Column(Integer, default=0)
    html_to_text_ratio = Column(Float, nullable=True)
    has_javascript = Column(Integer, default=0)
    has_iframes = Column(Integer, default=0)
    has_forms = Column(Integer, default=0)
    
    # Lexical features
    urgent_words = Column(Integer, default=0)
    financial_terms = Column(Integer, default=0)
    personal_info_requests = Column(Integer, default=0)
    
    # Stylometric features (for ML)
    avg_word_length = Column(Float, nullable=True)
    sentence_count = Column(Integer, default=0)
    exclamation_count = Column(Integer, default=0)
    question_count = Column(Integer, default=0)
    
    # Header anomalies
    display_name_mismatch = Column(Integer, default=0)
    reply_to_mismatch = Column(Integer, default=0)
    received_hops = Column(Integer, default=0)
    
    # Raw feature vector for ML (optional)
    feature_vector = Column(JSON, nullable=True)
    
    # Timestamps
    extracted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Feature for message {self.message_id}>"
