from datetime import datetime

from fastapi import Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import decode_access_token
from app.models.users import User
from app.core.database import get_async_session


# Pagination & Filters
def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
) -> Dict[str, int]:
    return {"skip": skip, "limit": limit}


def book_filters(
    title: str | None = Query(None),
    author: str | None = Query(None),
    published_year: int | None = Query(None),
    min_year: int | None = Query(None, ge=1500),
    # Fixed: removed hardcoded le=2026; now dynamically uses the current year
    max_year: int | None = Query(None, le=datetime.now().year)
) -> dict:
    return {
        "title": title,
        "author": author,
        "published_year": published_year,
        "min_year": min_year,
        "max_year": max_year,
    }


# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    statement = select(User).where(User.username == username)
    result = await session.exec(statement)
    user = result.first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user