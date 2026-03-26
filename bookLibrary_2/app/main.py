from fastapi import FastAPI
from .config import settings

from app.routers.general import router as general_router
from app.routers.books import router as books_router
#############################################################################################
#############################################################################################
#############################################################################################
app = FastAPI(
    title = "New Book Library",
    description = "New book library with simple CRUD operation in database sqlite",
    version = "1.0.0"
)
#############################################################################################
#############################################################################################
#############################################################################################
@app.get("/")
def home_route():
    return {"message": f"home route worls: {app.title}, {app.description}, {app.version}"}
@app.get("/settings")
def settings_route():
    return {"message": f"settings properly configured with database information: {settings.database_connection_url} and {settings.secret_key}"}
#############################################################################################
#############################################################################################

app.include_router(general_router)
app.include_router(books_router)

#############################################################################################

