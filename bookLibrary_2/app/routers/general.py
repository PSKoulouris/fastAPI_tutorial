from fastapi import APIRouter
from app.config import settings

router = APIRouter(
    tags=["General Routes"]
)

@router.get("/health", status_code=200)
async def heath_check():
    return {
            "message": "app works fine",
            "title": settings.title,
            "description":settings.description,
            "version": settings.version
    }