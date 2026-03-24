from fastapi import FastAPI
from pydantic import BaseModel, Field #field function for validation



app = FastAPI() #fast api object withput decription

#Create a class bluprint for the book:

class Book (BaseModel):
    id : int 
    title : str
    author : str
    year : int = Field (..., gt = 1000, le = 2100) #... means no default value 
    availbale : bool

#save the books in []
books_library = []
#
book_id_counter = 1
#CRUD end points: 

@app.get("/books") #path with skip and limit query parameter
def get_books(skip : int = 0, limit : int = 25):
    return books_library[skip : skip + limit] #create arange of books

@app.get("/books/{id}")
def get_book(id : int):
    for book in books_library:
        if book.id == id:
            return book 
    return {"message" : "Book not found"}

@app.post("/books")
def create_book(book : Book):
    global book_id_counter

    new_book = Book(
        id = book_id_counter,
        title = book.title,
        author = book.author,
        year = book.year,
        availbale = book.available
    )
    books_library.append(new_book)
    book_id_counter += 1
    return new_book

@app.put("/books/{id}")
def update_book(id : int, updatedBook : Book):
    for i, book in enumerate(books_library):
        if book.id == id: 
            updatedBook.id = book.id
            books_library[i] = updatedBook
            return updatedBook

#@app.patch()

#@app.delete("/books/{id}") 

