from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    username : str = Field(unique=True, index=True)
    email : str = Field(unique=True, index=True)
    hashed_password : str
    role : str = Field(default="user")
    is_active : bool = True
    created_at :datetime = Field(default_factory=datetime.utcnow) #datetime.now(datetime.timezone.utc)