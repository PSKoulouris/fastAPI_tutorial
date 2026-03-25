from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME : str ="Book Library API in settings"
    SECRET_KEY : str="this-is-my-secret-key337603"
    DATABASE_URL : str="sqlite+aiosqlite:///booklibrary.db"

    class Config:
        env_file = ".env"

settings = Settings()
