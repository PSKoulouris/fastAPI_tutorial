from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlmodel import Session #unique per user to keep the connection to database alive. completed cycle in core.database.py
from typing import List

from app.schemas.book import BookCreate,BookRead
from app.core.database import get_sync_session
#we will create the CRUDE operations separrately and import them
from app.crud.book import create_book, get_all_books, get_book_by_id, update_book, delete_book

from app.dependencies import pagination
###################################################################################

router = APIRouter(
    prefix = "/books",
    tags = ["books"]
)

async def log_action(message : str):
    print(f"[BACKGROUND LOG]: {message}")

@router.post("/", response_model=BookRead, status_code = 201)  
async def create_book_endpoint(
    book : BookCreate, #book of datatype BookCreate
    background_tasks : BackgroundTasks,
    session : Session = Depends(get_sync_session)
):
    db_book = create_book(session,book)      #CRUD folder required to simply code structure
    background_tasks.add_task(log_action, f"New Book created{book.title}")
    return db_book
    """
    final response of return db_book:
    title, author, isbn, description, published_year, if, cover_image
    """

@router.get("/", response_model=List[BookRead], status_code=200)
async def get_all_books_endpoint(
    pagination_params : dict = Depends(pagination),
    session: Session = Depends(get_sync_session)
):
    return get_all_books(
        session,
        skip = pagination_params["skip"],
        limit = pagination_params["limit"]
    )

@router.get("/{book_id}", response_model = BookRead, status_code=200)
async def get_book_endpoint(
    book_id : int, 
    session : Session = Depends(get_sync_session)
):
    book = get_book_by_id(session, book_id)

@router.put("/{book_id}", response_model=BookRead, status_code=200)
async def update_book_endpoint(
    book_id : int,
    updated_book : BookCreate,
    session : Session = Depends(get_sync_session)
):
    updated = update_book(session, book_id, updated_book)

    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")

    return updated

@router.delete("/{book_id}", status_code=204)
async def delete_book_endpoint(
    book_id : int,
    session : Session = Depends(get_sync_session)
):
    deleted = delete_book(session, book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return None



###################################################################################