#Python Packages
from sqlmodel import SQLModel, create_engine # Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession 

from typing import AsyncGenerator

#My own files
from app.config import settings
#####################################################################################################
#sync_url = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")

"""
engine = create_engine(
    sync_url,
    echo=False,
    connect_args={"check_same_thread": False} 
)
"""
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker[AsyncSession](
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)
def create_db_and_tables_sync():
    sync_url=settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite")
    engine=create_engine(sync_url)
    SQLModel.metadata.create_all(engine)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
    #session = Session(engine)
    #with session:
        #yield session
    """with Session(engine) as session:
        yield session"""
    