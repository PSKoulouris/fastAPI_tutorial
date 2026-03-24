# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'My API'
    debug: bool = False
    database_url: str

class Config:
   # env_file = '.env’
   model_config = SettingsConfigDict(env_file = ".env")


settings = Settings()

