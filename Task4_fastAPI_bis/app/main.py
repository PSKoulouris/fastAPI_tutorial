from fastapi import FastAPI
from app.config import settings
from app.routers import users, items, book

from app.core.database import create_db_and_tables

#########################################################################################
########################################################################################

app = FastAPI(
    title ="XBoost",
    description = "Xboost model to diagnose and prognose",
    version = "1.00"
)

########################################################################################
########################################################################################

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

########################################################################################
########################################################################################


app.include_router(users.router)
app.include_router(items.router)
app.include_router(book.router)

##########################################################################################
##########################################################################################

@app.get("/welcome")
def homeRoute():
    return {
        "message":f"""Welcome to the main page of XBoost fastAPI:
                    Title: {app.title}
                    Description: {app.description}
                    Version: {app.version}"""
    }
########################################################################################
@app.get("/variables")
def variablesRoute():
    return {"message2": f"Environment variables info: {settings.app_name},{settings.database_url},{settings.key}"}
########################################################################################
#Exercice 2:
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
############################################################################################################
############################################################################################################