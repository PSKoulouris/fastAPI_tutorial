from fastapi import Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from typing import Dict

from app.core.security import decode_access_token
from app.models.user import User
from app.core.database import get_async_session


def pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> Dict[str, int]:
    """Reusable pagination dependency"""
    return {"skip": skip, "limit": limit}


def book_filters(
    title: str | None = Query(None, description="Filter by title"),
    author: str | None = Query(None, description="Filter by author"),
    published_year: int | None = Query(None, description="Filter by published year"),
    min_year: int | None = Query(None, ge=1500),
    max_year: int | None = Query(None, le=2026)
) -> dict:
    """Reusable book filtering dependency"""
    return {
        "title": title,
        "author": author,
        "published_year": published_year,
        "min_year": min_year,
        "max_year": max_year
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session : AsyncSession = Depends(get_async_session)
) -> User :
    
    try:
        payload = decode_access_token(token)
        username : str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            ) 
    except Exception:
        raise HTTPException(
            status_code=401,
            detail= "Could not validate credentials"
        )
    
    statement = select(User).where(User.username == username)
    result = await session.exec(statement)

    user = result.first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
           status_code=400,
           detail="Inactive user" 
        )
    
    return user


async def get_current_admin(
    current_user : User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail = "Admin access only!"
        )
    return current_user