import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.main import app
from app.core.database import get_async_session
from app.models.book import Book
from app.models.users import User

# Sync URL for metadata create/drop; async URL must match the same file for tests.
TEST_SYNC_URL = "sqlite:///./test.db"
TEST_ASYNC_URL = "sqlite+aiosqlite:///./test.db"

sync_engine = create_engine(TEST_SYNC_URL)
async_engine = create_async_engine(TEST_ASYNC_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_session():
    async with AsyncSessionLocal() as session:
        yield session



@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables before tests run, drop them after."""
    SQLModel.metadata.create_all(sync_engine)
    yield
    SQLModel.metadata.drop_all(sync_engine)


@pytest.fixture
def client():
    """Give every test a fresh HTTP client connected to the test database."""
    app.dependency_overrides[get_async_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()



def test_get_all_books(client):
    response = client.get("/api/v1/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_book_unauthorized(client):
    response = client.post("/api/v1/books/", json={})
    assert response.status_code in [401, 422]
