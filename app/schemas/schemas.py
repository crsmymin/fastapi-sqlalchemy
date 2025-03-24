# schemas/schemas.py
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

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