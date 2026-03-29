from sqlmodel import Session
from app.schemas.book import BookCreate
from app.models.book import Book 

def create_book(session: Session, book_in : BookCreate) -> Book:
    db_book = Book.model_validate(book_in)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book



