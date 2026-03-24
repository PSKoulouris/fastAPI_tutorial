from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    app_name : str = "Task1 extended"
    debug : bool = False
    database_url : str = "sqlite:///./test.db"
    api_key : str = "testingAPIkey"

    class Config:
        env_file = ".env" 



settings = Settings()