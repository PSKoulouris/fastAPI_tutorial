from sqlmodel import select #Session
from sqlmodel.ext.asyncio import AsyncSession

from app.models.book import Book
from app.schemas.book import BookCreate, BookRead
from typing import List, Optional
######################################################################################################
#Function to create the book into the Book Table
async def create_book(session: AsyncSession, book_in : BookCreate) -> Book: 
    db_book = Book.model_validate(book_in)
    session.add(db_book) #Adding the Book in the DB Table 
    await session.commit() #Saving the changes done in the DB Table
    await session.refresh(db_book)
    return db_book

async def get_all_books(session : AsyncSession, skip : int = 0, limit : int = 10) -> List[Book]:
    #use the functions to select from the DB Table
    statement= select(Book).offset(skip).limit(limit)
    result =  await session.exec(statement) #The initial value is a "Promise"
    return result.all()


async def get_book_by_id(session:AsyncSession, book_id : int ) -> Optional[Book]:
    statement = select(Book).where(Book.id == book_id)
    result = await session.exec(statement)
    return result.first() 

async def update_book(
    session : AsyncSession, 
    book_id : int, 
    updated_book : BookCreate
) -> Optional[Book]:
    
    db_book = await get_book_by_id(session, book_id)
    if not db_book:
        return None

    for key,value in updated_book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    await session.commit()
    await session.refresh(db_book)

    return db_book

async def delete_book(session : AsyncSession, book_id : int) -> bool:
    db_book = await get_book_by_id(session, book_id)

    if not db_book:
        return False
    
    await session.delete(db_book)
    await session.commit()
    return True