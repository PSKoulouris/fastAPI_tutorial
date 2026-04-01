from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.database import get_async_session


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201)
async def register_user(
    user_in : UserCreate,
    session : AsyncSession = Depends(get_async_session)
):
    statement = select(User).where(
        (User.username == user_in.username) | (User.email == user_in.email)
    )
    result = await session.exec(statement)
    if result.first():
        raise HTTPException(status_code=400, detail="Username or eamil already exists")
    
    hashed_password = get_password_hash(user_in.password)
    user = User(
        username= user_in.username,
        email= user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {
        "message": "User registered successfully", 
        "username":user.username
    }

@router.post("/token")
async def login(
    form_data : OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    statement = select(User).where(
        User.username == form_data.username
    )

    result = await session.exec(statement)
    user = result.first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password or username",
            headers = {"Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub":user.username})
    return {"access_token":access_token, "token_type": "bearer"}