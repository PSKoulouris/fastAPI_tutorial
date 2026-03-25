from fastapi import FastAPI
from .config import settings

from app.core.database import create_db_and_tables

from app.routers.books import router as books_router
############################################################################################
app = FastAPI(
    title = "Book Library",
    description = "Book Library with FastAPI",
    version = "1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(books_router)

############################################################################################
#Create a book db varibal and initianalize it with an empty list:
#books_db = []


############################################################################################
@app.get("/", status_code=200)
async def root(): #uvicorn is an asycronous server so best pratice is to create async funct by default
    return {"message" : f"Welcome to our Application: {settings.APP_NAME}" }

@app.get("/health", status_code=200)
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version" :"1.0.0",
        "message" : "The Book Library is Running smoothly"
    }

"""
@app.get("/books")
async def get_books():
    return books_db

@app.post("/books")
async def create_book(book : dict):
    books_db.append(book)
    return book

@app.get("/books/search")
async def search_book(title : str):
    if not title: 
        return books_db
    return[b for b in books_db if title.lower() in b.get("title", "").lower()]

@app.get("/books/{book:id}")
async def get_book_by_id(book_id : int):
    pass    
"""
#############################################################################################
