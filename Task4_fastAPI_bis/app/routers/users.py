from fastapi import APIRouter
from app.config import settings
#############################################################################################
#############################################################################################
router = APIRouter(
    prefix="/users",
    tags=["users"]
)
#############################################################################################
#############################################################################################


@router.get("/health")
def read_health():
    return{"health status": "200 Ok!"}

@router.get("/config")
def read_config():
    if not settings.debug:
        print("error")
    return {
        "app_name": settings.app_name,
        "debug": "settings returned for API",
        "api-key": settings.api_key
    }
