from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional

from app.models.book import Book
from app.schemas.book import BookCreate


async def create_book(session: AsyncSession, book_in: BookCreate) -> Book:
    db_book = Book.model_validate(book_in)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

async def get_all_books(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    title: str | None = None,
    author: str | None = None,
    published_year: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
) -> List[Book]:
    statement = select(Book)

    if title:
        statement = statement.where(Book.title.ilike(f"%{title}%"))
    if author:
        statement = statement.where(Book.author.ilike(f"%{author}%"))
    if published_year:
        statement = statement.where(Book.published_year == published_year)
    if min_year:
        statement = statement.where(Book.published_year >= min_year)
    if max_year:
        statement = statement.where(Book.published_year <= max_year)

    statement = statement.offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()

async def get_book_by_id(session: AsyncSession, book_id: int) -> Optional[Book]:
    statement = select(Book).where(Book.id == book_id)
    result = await session.exec(statement)
    return result.first()

async def update_book(session: AsyncSession, book_id: int, book_in: BookCreate) -> Optional[Book]:
    db_book = await get_book_by_id(session, book_id)
    if not db_book:
        return None
    for key, value in book_in.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)
    return db_book

async def delete_book(session: AsyncSession, book_id: int) -> bool:
    db_book = await get_book_by_id(session, book_id)
    if not db_book:
        return False
    await session.delete(db_book)
    await session.commit()
    return True