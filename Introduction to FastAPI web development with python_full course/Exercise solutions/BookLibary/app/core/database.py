from sqlmodel import SQLModel,create_engine
from sqlmodel.ext.asyncio.session import AsyncSession 
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator

from app.config import settings


async_engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def create_db_and_tables_sync():
    sync_url = settings.DATABASE_URL.replace("sqlite+aiosqlite", "sqlite", 1)
    engine = create_engine(sync_url)
    SQLModel.metadata.create_all(engine)