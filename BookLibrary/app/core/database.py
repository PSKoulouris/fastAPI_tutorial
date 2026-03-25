from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

sync_url = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")

#create engine of the database:

engine = create_engine(
    sync_url,
    echo=False, #for asyncronous version of sqlite
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_sync_session():
    #session = Session(engine)
    #with session:
    #    yield session  
    with Session(engine) as session:
        yield session #yield is used to return the session without terminating the action like Return does.
        