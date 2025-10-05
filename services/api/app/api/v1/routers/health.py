"""Health check endpoints for monitoring service status."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.core.config import settings
from app.api.v1.dependencies.db import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """Quick health check - API is alive."""
    return {
        "status": "healthy",
        "service": "LazyMail Phishing Detection API",
        "version": "1.0.0"
    }


@router.get("/db")
async def health_check_database(db: AsyncSession = Depends(get_db)):
    """Check database connectivity."""
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return {
            "status": "healthy",
            "service": "PostgreSQL",
            "message": "Database connection successful"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "PostgreSQL",
            "error": str(e)
        }


@router.get("/rspamd")
async def health_check_rspamd():
    """Check Rspamd connectivity."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{settings.RSPAMD_HOST}:{settings.RSPAMD_PORT}/ping",
                timeout=5.0
            )
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "service": "Rspamd",
                "message": response.text
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Rspamd",
            "error": str(e)
        }


@router.get("/all")
async def health_check_all(db: AsyncSession = Depends(get_db)):
    """Check all services at once."""
    results = {
        "api": {"status": "healthy"},
        "database": {"status": "unknown"},
        "rspamd": {"status": "unknown"}
    }
    
    # Check database
    try:
        await db.execute(text("SELECT 1"))
        results["database"] = {"status": "healthy"}
    except Exception as e:
        results["database"] = {"status": "unhealthy", "error": str(e)}
    
    # Check Rspamd
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{settings.RSPAMD_HOST}:{settings.RSPAMD_PORT}/ping",
                timeout=5.0
            )
            results["rspamd"] = {"status": "healthy" if response.status_code == 200 else "unhealthy"}
    except Exception as e:
        results["rspamd"] = {"status": "unhealthy", "error": str(e)}
    
    # Overall status
    all_healthy = all(svc.get("status") == "healthy" for svc in results.values())
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "services": results
    }
