from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class ArticleCreate(BaseModel):
  title: str
  content: str
  description: str

  @field_validator('title', 'content', 'description')
  def check_empty(cls, v):
    if v == '':
        raise ValueError('This field cannot be empty')
    return v
    
class ArticleUpdate(BaseModel):
  title: Optional[str] = None  
  content: Optional[str] = None
  description: Optional[str] = None

  @field_validator('title', 'content', 'description')
  def check_empty(cls, v):
    if v == '':
        raise ValueError('This field cannot be empty')
    return v

class ArticleResponse(BaseModel):
  id: int
  title: Optional[str] = None
  description: Optional[str] = None
  content: str
  user_id: int
  created_at: datetime
  updated_at: Optional[datetime] = None
  class Config:
    from_attributes = True