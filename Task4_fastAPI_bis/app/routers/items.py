from fastapi import APIRouter
from app.config import settings
#from app.main import app
#############################################################################################
#############################################################################################
router = APIRouter(
    prefix = "/items",
    tags = ["items"]
)
#############################################################################################
#############################################################################################

"""@router.get("/about")
def read_about():
    return {"Title" : app.title,
            "Version": app.version,
            "Description":app.description
            }
cannot import app for information->use settings
"""

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