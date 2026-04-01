from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from .env file using Pydantic v2"""
    
    APP_NAME: str = Field(default="FastAPI Application", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    DATABASE_URL: str = Field(default="sqlite:///./test.db", description="Database connection URL")
    API_KEY: str = Field(default="secret-key-dev", description="API key for authentication")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create a global settings instance
settings = Settings()
