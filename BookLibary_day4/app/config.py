from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME : str ="Book Libary API"
    SECRET_KEY : str = "this-is-my-secret-key12345"
    DATABASE_URL : str = "sqlite+aiosqlite:///booklibary.db"
    
    class config:
        env_file =".env"

settings = Settings()