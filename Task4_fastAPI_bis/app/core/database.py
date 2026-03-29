from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

#######################################################################
#######################################################################

sync_url = settings.database_url.replace("sqlite+aiosqlite","sqlite")

engine = create_engine( 
    sync_url,
    echo = False,
    connect_args = {"check_same_thread" : False}
)

#######################################################################
#######################################################################

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_sync_session():
    with Session(engine) as session:
        yield session   



