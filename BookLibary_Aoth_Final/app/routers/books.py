from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession #Session #completed cycle in core.database.py

from typing import List
from app.core.database import get_async_session
from app.schemas.book import BookCreate, BookRead
from app.crud.book import create_book, get_all_books, get_book_by_id, update_book, delete_book
from app.dependencies import pagination

# We will create the CRUD operation sepratly and import them

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

 

async def log_action(message : str):
    print(f"[BACKGROUND LOG]: {message}")

 

@router.post("/", response_model=BookRead, status_code=201)
async def create_book_endpoint(
    book : BookCreate,
    background_tasks : BackgroundTasks,
    session : AsyncSession = Depends(get_async_session)
):

    #CRUD folder, required to simplify the code structure!
    db_book = await create_book(session,book) #create_book(book_in= book, session=session)
    background_tasks.add_task(log_action, f"New Book created{book.title}")
    return db_book
    #Example of the final response key-value pairs:

    """

    title, author, isbn, description, published_year, id, cover_image

    """

 

@router.get("/", response_model=List[BookRead], status_code=200)
async def get_all_books_endpoint(
    pagination_params : dict = Depends(pagination),
    session: AsyncSession = Depends(get_async_session)
):

    skip = pagination_params["skip"],
    limit = pagination_params["limit"]
    return  await get_all_books(
        session,
        skip = skip,
        limit = limit
    )

 
@router.get("/{book_id}", response_model=BookRead, status_code=200) #Using Path Parameter [book id]
async def get_book_endpoint(
    book_id : int,
    session : AsyncSession = Depends(get_async_session)
):
    book = await get_book_by_id(session, book_id) # crud > book.py
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

 

@router.put("/{book_id}", response_model=BookRead, status_code= 200)
async def update_book_endpoint(
    book_id : int,
    updated_book : BookCreate,
    session : AsyncSession = Depends(get_async_session)
):
    updated = await update_book(session, book_id, updated_book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not Found!")
    return updated

 

@router.delete("/{book_id}", status_code=204)
async def delete_book_endpoint(
    book_id : int,
    session : AsyncSession = Depends(get_async_session)
):
    deleted = await delete_book(session, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book Not Found!")
    return None


"""

Sync Version : def delete_book() -> to call it : delete_book()

Async Version : def delete_book() -> to call it : await delete_book()

"""


