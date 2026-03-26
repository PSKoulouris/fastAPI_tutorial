from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    title : str = "New Book Library"
    description : str = "New book library with simple CRUD operation in database sqlite"
    version : str = "1.0.0"
    database_connection_url:str
    secret_key:str

    class Config:
        env_file = ".env"

settings = Settings()

