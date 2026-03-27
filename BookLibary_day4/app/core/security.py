from fastapi import HTTPException, status
from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext

from app.config import settings


"""
JSON web token{
    header
    payload
    signature}

"""

pw_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")



def verify_password(plain_password : str, hashed_password : str) -> bool:
    return pw_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pw_context.hash(password)

def create_access_token( data : dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    #to_encode["expire" = expire]
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

    

def decode_access_token(token : str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"Authenticate": "Bearer"} # means use jason web token "Bearer"
        )