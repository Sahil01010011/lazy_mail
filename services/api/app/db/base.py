"""
Import all models here so Alembic can detect them.
"""
from app.core.database import Base
from app.db.models.message import Message
from app.db.models.verdict import Verdict
from app.db.models.feature import Feature

# Export Base for Alembic
__all__ = ["Base", "Message", "Verdict", "Feature"]
