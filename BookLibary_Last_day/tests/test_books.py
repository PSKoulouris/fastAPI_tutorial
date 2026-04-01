#Testing tool for automation
import pytest
#from fastapi.testclient import TestClient #alwasy for syncronous version
#httpx for asnyc test
from httpx import AsyncClient, ASGITransport
#from sqlmodel import SQLModel, create_engine, Session # Use the syncronous version for pytest

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
#from app.core.database import get_async_session
from app.models.book import Book
from app.models.user import User


#Create a variable for a diferent database

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db" 

#create functions to test:

#create a new engine to test
engine = create_async_engine(TEST_DATABASE_URL, echo=False)

TestSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

#override get_sync_session()
def override_get_async_session():
    with TestSessionLocal() as session:
        yield session

#apply the test with fixture()
@pytest.fixture(scope ="session", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest.fixture
async def client():
    app.dependency_overrides[get_async_session] = override_get_async_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test")
        yield c


@pytest.mark.asyncio
async def test_get_all_books(client):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200 #assert means anything on the right is assumed
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_book_unauthorized(client):
    response = client.post("/api/v1/books/", json={}) #Trying to create an empty book
    assert response.status_code in [401,422]





