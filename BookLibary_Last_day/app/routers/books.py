from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, UploadFile , File, Form
from sqlmodel.ext.asyncio.session import AsyncSession #Session #completed cycle in core.database.py
import shutil #used to interact with files/built-in

from typing import List, Optional
from app.core.database import get_async_session
from app.schemas.book import BookCreate, BookRead
from app.crud.book import create_book, get_all_books, get_book_by_id, update_book, delete_book
from app.dependencies import pagination, get_current_admin, get_current_user

# We will create the CRUD operation sepratly and import them
################################################################################################################
################################################################################################################
################################################################################################################

router = APIRouter(
    prefix="/books",
    tags=["books"]
)
################################################################################################################
################################################################################################################
 
#Backgroundtask:
async def log_action(message : str):
    print(f"[BACKGROUND LOG]: {message}")

################################################################################################################
################################################################################################################ 

# ============================= PUBLIC ROUTES ==================================================================
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

"""
    title, author, isbn, description, published_year, id, cover_image
"""

################################################################################################################ 
# ============================= PROTECTED ROUTES ======================================================


@router.post("/", response_model=BookRead, status_code=201)
async def create_book_endpoint(
    #book : BookCreate,  #update for security with the book informations bellow
    background_tasks : BackgroundTasks,
    session : AsyncSession = Depends(get_async_session),
    current_admin = Depends(get_current_admin),
    title : str = Form(..., min_length=1, max_length=200),
    author : str = Form(..., min_length=1, max_length=100),
    isbn : str = Form(..., min_length=10, max_length=13),
    published_year : int = Form(..., ge=1500),
    description : Optional[str] = Form(None, max_length=1000),
    cover : UploadFile = File(...)
):

    #CRUD folder, required to simplify the code structure!
    #db_book = await create_book(session,book) #create_book(book_in= book, session=session)
    file_extension = cover.filename.split(".")[-1].lower() #split the filename at . , access it at the end of teh array, and tranform i  lowercase
    filename = f"{isbn}.{file_extension}"
    file_path = f"static/covers/{filename}"

    with open(file_path, "wb") as directory:
        shutil.copyfileobj(cover.file, directory)
    
    book = BookCreate(
        title = title,
        author= author,
        isbn = isbn,
        published_year= published_year,
        description=description,
        cover_image = f"/covers/{filename}"
    )

    db_book = await create_book(session,book) #create_book(book_in= book, session=session)
    background_tasks.add_task(log_action, f"New Book created{book.title}")
    return db_book

 

@router.put("/{book_id}", response_model=BookRead, status_code= 200)
async def update_book_endpoint(
    book_id : int,
    updated_book : BookCreate,
    session : AsyncSession = Depends(get_async_session),
    current_admin = Depends(get_current_admin)
):
    updated = await update_book(session, book_id, updated_book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not Found!")
    return updated


@router.delete("/{book_id}", status_code=204)
async def delete_book_endpoint(
    book_id : int,
    session : AsyncSession = Depends(get_async_session),
    current_admin = Depends(get_current_admin)
):
    deleted = await delete_book(session, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book Not Found!")
    return None


"""

Sync Version : def delete_book() -> to call it : delete_book()

Async Version : def delete_book() -> to call it : await delete_book()

"""


