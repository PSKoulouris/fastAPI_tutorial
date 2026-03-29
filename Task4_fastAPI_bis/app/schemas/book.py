from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime 

current_year = datetime.now().year

class BaseBook(BaseModel):
    title : str = Field(..., min_length=1, max_length=200)
    author : str = Field(..., min_length=1, max_length=200)
    isbn : str = Field(..., min_length=10, max_length=13)
    description : Optional[str] = Field(None, max_length= 1000)
    published_year : int = Field(..., ge = 1500, le = current_year)

class BookCreate(BaseBook):
    pass
class BookRead(BaseBook):
    id : int 



