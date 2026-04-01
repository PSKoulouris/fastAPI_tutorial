from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Book Library API"  # Fixed: typo "Libary" → "Library"

    # Fixed: No hardcoded default — SECRET_KEY must be provided via .env
    # Add to your .env file: SECRET_KEY=your-very-secret-key-here
    SECRET_KEY: str

    DATABASE_URL: str = "sqlite+aiosqlite:///booklibary.db"


settings = Settings()