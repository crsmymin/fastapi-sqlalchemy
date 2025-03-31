from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
  name: str
  @field_validator('name')
  def check_empty(cls, v):
      if v == '':
          raise ValueError('This field cannot be empty')
      return v
  
class CategoryUpdate(BaseModel):
  name: Optional[str] = None
  @field_validator('name')
  def check_empty(cls, v):
      if v == '':
          raise ValueError('This field cannot be empty')
      return v
  
class CategoryResponse(BaseModel):
  id: int
  name: str
  created_at: datetime
  updated_at: Optional[datetime] = None
  class Config:
    from_attributes = True