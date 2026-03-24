from fastapi import FastAPI
#import settings from config
from config import settings

app = FastAPI(
    title = "My Api project numner 1",
    description = "a sample fastapi application",
    version = "1.0.1"
)

@app.get("/")  #.get GET request
def first_route():
    return {"message":"First FastAPI project created successfully"}

@app.get("/info")
def app_info():
    return {"appName" : settings.app_name}

