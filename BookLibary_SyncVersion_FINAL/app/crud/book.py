from sqlmodel import Session, select
from app.models.book import Book
from app.schemas.book import BookCreate, BookRead
from typing import List, Optional

#Function to create the book into the Book Table
def create_book(session: Session, book_in : BookCreate) -> Book: 
    db_book = Book.model_validate(book_in)
    session.add(db_book) #Adding the Book in the DB Table 
    session.commit() #Saving the changes done in the DB Table
    session.refresh(db_book)
    return db_book

def get_all_books(session : Session, skip : int = 0, limit : int = 10) -> List[Book]:
    #use the functions to select from the DB Table
    statement= select(Book).offset(skip).limit(limit)
    return session.exec(statement).all()


def get_book_by_id(session:Session, book_id : int ) -> Optional[Book]:
    statement = select(Book).where(Book.id == book_id)
    return session.exec(statement).first()

def update_book(
    session : Session, 
    book_id : int, 
    updated_book : BookCreate
) -> Optional[Book]:
    
    db_book = get_book_by_id(session, book_id)
    if not db_book:
        return None

    for key,value in updated_book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book

def delete_book(session : Session, book_id : int) -> bool:
    db_book = get_book_by_id(session, book_id)

    if not db_book:
        return False
    
    session.delete(db_book)
    session.commit()
    return True