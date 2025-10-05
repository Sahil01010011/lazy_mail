"""Database session dependency for FastAPI routes."""
from app.core.database import get_db

# Re-export for cleaner imports
__all__ = ["get_db"]
