"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# Get the project root (go up from services/api/app/core/ to project root)
ROOT_DIR = Path(__file__).resolve().parents[4]
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    APP_NAME: str = "LazyMail Phishing Detection"
    DEBUG: bool = True
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # Rspamd
    RSPAMD_HOST: str = "localhost"
    RSPAMD_PORT: int = 11334
    RSPAMD_CONTROLLER_PASSWORD: Optional[str] = None
    
    @property
    def database_url(self) -> str:
        """Construct async database URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def sync_database_url(self) -> str:
        """Construct sync database URL for Alembic migrations."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = True
        extra = "ignore"


settings = Settings()
