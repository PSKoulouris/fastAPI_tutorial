from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session

from app.schemas.book import BookRead, BookCreate
from app.core.database import get_sync_session
from app.crud.book import create_book

################################################################################

router = APIRouter(
    tags=["Books"]
)

################################################################################
#Define backround log function for backgroundtasks in CRUD
def log_action(message : str):
    print(f"[BACKGROUND LOG] : {message}")


@router.post("/", response_model= BookRead, status_code=201)
async def create_book_endpoint(
    book : BookCreate,
    background_tasks : BackgroundTasks,
    session: Session = Depends(get_sync_session)
):
    db_book = create_book(session,book)
    background_tasks.add_task(log_action, f"Book record created in the database under: {book.title}")
    return db_book