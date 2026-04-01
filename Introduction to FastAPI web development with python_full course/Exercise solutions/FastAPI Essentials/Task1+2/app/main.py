from fastapi import FastAPI, Query
from app.config import settings

app = FastAPI(
    title = "Task 1",
    description = "Starting up",
    version = "1.0.0",
    docs_url = "/docs" 
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Dear "}

@app.get("/about")
def read_about():
    return {
        "Title": app.title, 
        "Version": app.version, 
        "Description":app.description
    }

@app.get("/health")
def read_health():
    return {
        "health status": "200 OK! :)"
    }


@app.get("/config")
def read_config():
    if not settings.debug:
        print("error")
    return {
        "app-name": settings.app_name,
        "debug": settings.debug,
        "api-key": settings.api_key
    }


# Required query parameter
@app.get('/search')
def search(q: int = Query(ge=0)):
    return {'query': q}
    
