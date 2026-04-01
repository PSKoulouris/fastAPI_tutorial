import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.database import create_db_and_tables_sync
from app.core.middleware import RequestTimingMiddleware
from app.routers.books import router as books_router
from app.routers.auth import router as auth_router


# Fixed: replaced deprecated @app.on_event("startup") with lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fixed: ensure static/covers directory exists before mounting StaticFiles
    os.makedirs("static/covers", exist_ok=True)
    create_db_and_tables_sync()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Learn FastAPI by building a BookLibrary API",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    lifespan=lifespan,
)

# Static files
app.mount("/covers", StaticFiles(directory="static/covers"), name="covers")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(RequestTimingMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Internal Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "success": False}
    )

# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(books_router, prefix="/api/v1")