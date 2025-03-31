# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import user
from typing import List
from databases import get_db
from services import users  # 서비스 레이어 임포트

router = APIRouter(
  prefix="/api",
  tags=["users"],
  responses={404: {"description": "Not found"}},
)

@router.post("/users/", response_model=user.UserResponse)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    user_data = user.model_dump()
    new_user, error = users.create_user_service(user_data, db)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_user

@router.get("/users/{user_id}", response_model=user.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user_service(user_id, db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[user.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users.get_users_service(skip, limit, db)
    return users

@router.put("/users/{user_id}", response_model=user.UserResponse)
def update_user(user_id: int, user: user.UserUpdate, db: Session = Depends(get_db)):
    update_data = user.model_dump(exclude_unset=True)
    updated_user = users.update_user_service(user_id, update_data, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", response_model=user.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = users.delete_user_service(user_id, db)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user