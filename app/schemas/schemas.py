# schemas/schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username', 'email', 'password')
    def check_empty(cls, v):
        if v == '':
            raise ValueError('This field cannot be empty')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ArticleCreate(BaseModel):
    title: str
    content: str
    description: str
    user_id: int

class ArticleResponse(BaseModel):
    id: int
    title: str
    description: str
    content: str
    user_id: int
    created_at: datetime
    class Config:
        from_attributes = True