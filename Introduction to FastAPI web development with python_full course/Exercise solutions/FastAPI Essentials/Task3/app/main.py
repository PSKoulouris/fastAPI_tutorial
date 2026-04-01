from fastapi import FastAPI
from datetime import datetime
from app.config import settings
from app.routers import users
from app.routers import items

app = FastAPI(
    title=settings.APP_NAME,
    description="A simple FastAPI application with multiple routes",
    version="1.0.0"
)

# Register the routers
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI",
        "status": "running"
    }


@app.get("/about")
async def about():
    return {
        "app_name": "FastAPI Application",
        "description": "A simple FastAPI application with multiple routes",
        "version": "1.0.0",
        "author": "FastAPI Developer",
        "created_date": "2026-03-23"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FastAPI Application"
    }


@app.get("/config")
async def get_config():
    """
    Returns non-sensitive configuration values.
    Only accessible when DEBUG=True
    """
    if not settings.DEBUG:
        return {
            "error": "Config endpoint not available",
            "detail": "DEBUG mode is disabled"
        }
    
    return {
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL,
        # Note: API_KEY is intentionally excluded for security
    }
