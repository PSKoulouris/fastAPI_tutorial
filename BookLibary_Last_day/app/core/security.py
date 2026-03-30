from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
#from passlib.context import CryptContext #srated with this version
#Newer version to use: bcrypt inbuild package in python (always up to date or available)
import bcrypt

from app.config import settings

"""
    JSON Web Token{
        "header":{
            "alg":"HS256",
            "type" :"JWT"
        },
        "payload":{
            ...data
        },
        "signature":{
            header + payload + secret key
        }        
    
    }
"""

#passlib package:
#pw_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") #password pw context

#replace with bycrypt in all following functions: 

def verify_password(plain_password : str, hashed_password : str) -> bool:
    #return pw_context.verify(plain_password, hashed_password)
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def get_password_hash(password : str):
    #return pw_context.hash(password)
    salt = bcrypt.gensalt() #gensalt() generates random bytes and is used to encode the password
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8") # hashpw takes 2 parameters, the password in bytes and salt in bytes
    

def create_access_token( data : dict) -> str:
    to_encode = data.copy() #copy data to avoid altering the original information(best practice)
    #expire = datetime.utcnow() + timedelta(minutes=30) #time for token expiration
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp" : expire}) #to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token : str): #Decode token to determine if access should be granted or not 
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"Authenticate": "Bearer"}#optional 
        )