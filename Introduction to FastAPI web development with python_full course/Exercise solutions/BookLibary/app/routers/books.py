from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, UploadFile, File, Form
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
import shutil


from app.schemas.book import BookCreate, BookUpdate, BookRead
from app.crud.book import create_book, get_all_books, get_book_by_id, update_book, delete_book
from app.dependencies import pagination, book_filters, get_current_admin
from app.core.database import get_async_session

router = APIRouter(prefix="/books", tags=["books"])


async def log_action(message: str):
    print(f"[BACKGROUND LOG] {message}")


# ====================== Cached function for book retrieval ======================

async def cached_get_books(
    session,
    skip: int,
    limit: int,
    title: str | None,
    author: str | None,
    published_year: int | None,
    min_year: int | None,
    max_year: int | None
) -> List[dict]:
    return await get_all_books(
        session,
        skip=skip,
        limit=limit,
        title=title,
        author=author,
        published_year=published_year,
        min_year=min_year,
        max_year=max_year,
    )

# ====================== PUBLIC ROUTES ======================

@router.get("/", response_model=List[BookRead], status_code=200)
async def get_all_books_endpoint(
    pagination_params: dict = Depends(pagination),
    filters: dict = Depends(book_filters),
    session: AsyncSession = Depends(get_async_session)
):
    """Get books with pagination — demonstration of caching concept"""
    books = await cached_get_books( #using the crud function directly!!
        session=session,
        skip=pagination_params["skip"],
        limit=pagination_params["limit"],
        title=filters.get("title"),
        author=filters.get("author"),
        published_year=filters.get("published_year"),
        min_year=filters.get("min_year"),
        max_year=filters.get("max_year"),
    )
    return books


@router.get("/{book_id}", response_model=BookRead, status_code=200)
async def get_book_endpoint(
    book_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a single book by ID (Public)"""
    book = await get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ====================== ADMIN ONLY ROUTES ======================

@router.post("/", response_model=BookRead, status_code=201)
async def create_book_endpoint(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    current_admin=Depends(get_current_admin),
    title: str = Form(..., min_length=1, max_length=200),
    author: str = Form(..., min_length=1, max_length=100),
    isbn: str = Form(..., min_length=10, max_length=13),
    published_year: int = Form(..., ge=1500),
    description: Optional[str] = Form(None, max_length=1000),
    cover: UploadFile = File(...),
):
    """Create a new book with a cover image (Admin only)"""
    file_extension = cover.filename.split(".")[-1].lower()
    filename = f"{isbn}.{file_extension}"
    file_path = f"static/covers/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(cover.file, buffer)

    book_in = BookCreate(
        title=title,
        author=author,
        isbn=isbn,
        published_year=published_year,
        description=description,
        cover_image=f"/covers/{filename}",
    )

    db_book = await create_book(session, book_in)
    background_tasks.add_task(log_action, f"New book created: {title}")
    return db_book


@router.put("/{book_id}", response_model=BookRead, status_code=200)
async def update_book_endpoint(
    book_id: int,
    book_in: BookUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_admin=Depends(get_current_admin)
):
    """Update a book (Admin only)"""
    updated = await update_book(session, book_id, book_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/{book_id}", status_code=204)
async def delete_book_endpoint(
    book_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_admin=Depends(get_current_admin)
):
    """Delete a book (Admin only)"""
    deleted = await delete_book(session, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None