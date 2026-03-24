from fastapi import FastAPI
#import settings from config
from app.config import settings

##########################################################################
app = FastAPI(
    title = "Task1",
    description = "starting metadata",
    version = "1.0.2",
    docs_url = "/docs"
)
###########################################################################

@app.get("/")  #.get GET request
def read_root():
    return {"message":"Welcome to FastApi Task1"} 


@app.get("/about")
def read_about():
    return {"Title" : app.title,
            "Version": app.version,
            "Description":app.description
            }

@app.get("/health")
def read_health():
    return{"health status": "200 Ok!"}

@app.get("/config")
def read_config():
    if not settings.debug:
        print("error")
    return {
        "app_name": settings.app_name,
        "debug": "settings returned for API",
        "api-key": settings.api_key
    }