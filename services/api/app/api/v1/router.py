"""Main v1 API router that combines all endpoint routers."""
from fastapi import APIRouter

from app.api.v1.routers import health, messages

# Create v1 router
api_router = APIRouter(prefix="/v1")

# Include all sub-routers
api_router.include_router(health.router)
api_router.include_router(messages.router)

# You'll add more routers here as we build them:
# api_router.include_router(verdicts.router)
# api_router.include_router(analytics.router)
# api_router.include_router(actions.router)
