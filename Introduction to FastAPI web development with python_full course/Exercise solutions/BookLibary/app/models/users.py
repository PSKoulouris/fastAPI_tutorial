from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")   # "user" or "admin"
    is_active: bool = True
    # Fixed: replaced deprecated datetime.utcnow with datetime.now(timezone.utc)
    created_at: datetime = Field(default_factory=datetime.utcnow)