from pydantic import BaseModel, Field, EmailStr

#Create User class 

class UserCreate(BaseModel):
    username : str = Field(..., min_length=3, max_length=50)
    email : EmailStr
    password : str = Field(..., min_length=6)
    role : str = Field(default = "user", pattern="^(user|admin)$") #start wit ^, $ nothing more in Regex