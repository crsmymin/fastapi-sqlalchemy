from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from app.schemas.category_schema import CategoryResponse
from app.schemas.comment_schema import CommentResponse

class ArticleCreate(BaseModel):
    title: str
    content: str
    description: str
    category_ids: Optional[List[int]] = None

    @field_validator('title', 'content', 'description')
    def check_empty(cls, v):
        if v == '':
            raise ValueError('This field cannot be empty')
        return v
        
class ArticleUpdate(BaseModel):
    title: Optional[str] = None  
    content: Optional[str] = None
    description: Optional[str] = None
    category_ids: Optional[List[int]] = None

    @field_validator('title', 'content', 'description')
    def check_empty(cls, v):
        if v == '':
            raise ValueError('This field cannot be empty')
        return v

class ArticlesResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    categories: List[CategoryResponse] = []
    class Config:
        from_attributes = True

class ArticleResponse(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    content: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[CommentResponse] = []
    categories: List[CategoryResponse] = []
    class Config:
        from_attributes = True