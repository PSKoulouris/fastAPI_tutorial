from sqlmodel import SQLModel, Field
from typing import Optional

class Book(SQLModel, table = True):
    id : Optional[int] = Field(default=None, primary_key=True) #primary key is unique and never none
    title : str
    author : str
    isbn : str = Field(unique=True)
    description : Optional[str] = None
    published_year : int
    cover_image : Optional[str] = None

    