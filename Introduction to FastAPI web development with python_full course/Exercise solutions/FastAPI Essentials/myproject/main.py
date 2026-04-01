from fastapi import FastAPI
from config import settings

app = FastAPI(
    title= "My first FastAPI Project",
    description = "Trying Fast Api",
    version="1.0.1"
)

@app.get("/")
def first_route():
    return {"message": "You have Created successfully you First FastApi project"}

@app.get("/info")
def app_info():
    return {"appName": settings.app_name}