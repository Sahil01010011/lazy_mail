"""
LazyMail Phishing Detection API
Main FastAPI application entry point.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.database import engine
from app.api.v1.router import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    Called when FastAPI starts and stops.
    """
    # Startup
    logger.info("Starting LazyMail API...")
    logger.info(f"Database: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Shutting down LazyMail API...")
    await engine.dispose()
    logger.info("Database connections closed")


# Create FastAPI application
app = FastAPI(
    title="LazyMail Phishing Detection API",
    description="""
    Advanced email security platform with multi-layer phishing detection.
    
    ## Current Features (v0.3.0 - Layer 3)
    * **Complete email parsing**: MIME parsing with header/body/attachment extraction
    * **Authentication verification**: SPF/DKIM/DMARC checks
    * **URL analysis**: Threat detection, homograph attacks, suspicious TLDs
    * **HTML sanitization**: Risk scoring and dangerous element removal
    * **Database storage**: Messages, verdicts, and features for ML
    
    ## Coming Soon (Layers 4-5)
    * **ML classification**: Phishing and spam detection models
    * **Rspamd integration**: Advanced spam scoring
    * **Stylometry analysis**: BEC detection
    * **Automated ingestion**: Gmail/IMAP integration
    * **Real-time processing**: Celery workers
    * **Authentication**: JWT token-based authentication
    """,
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Include API router
app.include_router(api_router, prefix="/api")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": "LazyMail Phishing Detection API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health/all"
    }


# Custom 404 handler
@app.get("/{full_path:path}", include_in_schema=False)
async def catch_all(full_path: str):
    """Catch-all route for undefined endpoints."""
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Endpoint not found: /{full_path}",
            "available_docs": "/docs"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )
