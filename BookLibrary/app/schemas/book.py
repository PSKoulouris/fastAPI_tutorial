from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    title : str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn : str = Field(..., min_length=10, max_length=13)
    description : Optional[str] = Field(None, max_length=1000)
    published_year : int = Field(..., ge = 15000, le=2026) #or use datetime.now()

class BookCreate(BookBase): #inherite BookBase in case further information are needed in the future
    #price: float = Field(..., ge=0)
    pass

class BookRead(BookBase):
    id : int
    cover_image : Optional[str] = None #upgraded later



