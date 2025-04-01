from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.databases import get_db
from app.schemas import user_schema
from app.services import user_service  
from typing import List

router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/users/", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    new_user = user_service.create_user_service(user_data, db)
    return new_user

@router.get("/users/{user_id}", response_model=user_schema.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_service(user_id, db)

@router.get("/users/", response_model=List[user_schema.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_users_service(skip, limit, db)

@router.put("/users/{user_id}", response_model=user_schema.UserResponse)
def update_user(user_id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    update_data = user.model_dump(exclude_unset=True)
    updated_user = user_service.update_user_service(user_id, update_data, db)
    return updated_user

@router.delete("/users/{user_id}", response_model=user_schema.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user_service(user_id, db)