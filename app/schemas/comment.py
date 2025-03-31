from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
  content: str
  @field_validator('content')
  def check_empty(cls, v):
      if v == '':
          raise ValueError('This field cannot be empty')
      return v
  
class CommentUpdate(BaseModel):
  content: Optional[str] = None
  @field_validator('content')
  def check_empty(cls, v):
      if v == '':
          raise ValueError('This field cannot be empty')
      return v
  
class CommentResponse(BaseModel):
  id: int
  content: str
  article_id: int
  user_id: int
  created_at: datetime
  updated_at: Optional[datetime] = None