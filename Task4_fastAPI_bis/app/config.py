from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = 'My API'
    api_key: str = "api key assigned in settings"
    debug: bool = False
    database_url: str
    key: str

    model_config = SettingsConfigDict(env_file = ".env")


settings = Settings()