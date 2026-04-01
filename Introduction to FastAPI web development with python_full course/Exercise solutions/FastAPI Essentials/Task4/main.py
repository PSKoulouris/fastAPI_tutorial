from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book(BaseModel):
    id : int
    title : str
    author : str
    year : int = Field(..., ge=1000, le=2100)
    available : bool 

books_libary = []
book_id_counter = 1


@app.get("/books/") #query param added
def get_books(skip : int = 0, limit : int = 25):
    return books_libary[skip : skip + limit]


@app.get("/books/{id}")
def get_book(id : int):
    for book in books_libary:
        if book.id == id:
            return book
    return {"message": "Book Not found!"}

@app.post("/books")
def create_book(book : Book):
    global book_id_counter
    
    new_book = Book(
        id = book_id_counter,
        title = book.title,
        author = book.author,
        year = book.year,
        available = book.available
    )

    books_libary.append(new_book)
    book_id_counter +=1

    return new_book

@app.put("/books/{id}")
def update_book(id : int, updatedBook : Book):
    for i, book in enumerate(books_libary):
        if book.id == id:
            updatedBook.id = book.id
            books_libary[i] = updatedBook
            return updatedBook

#@app.patch()

#@app.delete("/books/{id}")