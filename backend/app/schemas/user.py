from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = Field(None, max_length=20)
    profession: Optional[str] = Field(None, max_length=255)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    profession: Optional[str] = None

class UserSignin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    profession: Optional[str] = None

class UserSignupResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str

class UserSigninResponse(BaseModel):
    user: UserResponse
    message: str

class UserSignoutResponse(BaseModel):
    message: str

