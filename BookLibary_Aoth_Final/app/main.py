from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from app.core.database import create_db_and_tables_sync
from app.routers.books import router as books_router
from app.routers.auth import router as auth_router
from app.core.middleware import RequestTimingMiddleware

app = FastAPI(
    title =settings.APP_NAME,
    description="Creating a Book Libary Project Course",
    version="1.0.0",
    openai_url="/api/v1/openai.json",
    docs_url = "/api/v1/docs"
)

@app.on_event("startup") #This became old could become unfunctional at any time
def on_startup():
    create_db_and_tables_sync()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print("INTERNAL SERVER ERROR")
    return JSONResponse(
        status_code = 500,
        content = {"detail":"Insernal server error"}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(RequestTimingMiddleware)

app.include_router(auth_router)
app.include_router(books_router)

#books_db = []

@app.get("/", status_code=200)
async def root():
    return {"message": f"Welcom to our Application:{settings.APP_NAME}"}

@app.get("/health", status_code=200)
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version" : "1.0.0",
        "message" : "The Book Linary is Running Smoothly!"
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
    return [ b for b in books_db if title.lower() in b.get("title", "").lower()]

@app.get("/books/{book_id}")
async def get_book_by_id(book_id : int):
    pass
"""