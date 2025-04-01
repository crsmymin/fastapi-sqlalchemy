from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.utils.utils import hash_password

def create_user_service(user_data: dict, db: Session):
    # 중복 사용자 체크
    existing_user = db.query(models.User).filter(models.User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user_data.get("password"))
    new_user = models.User(
        username=user_data.get("username"),
        email=user_data.get("email"),
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_service(user_id: int, db: Session):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_users_service(skip: int, limit: int, db: Session):
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_service(user_id: int, update_data: dict, db: Session):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 비밀번호 업데이트 시 해싱 처리
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_service(user_id: int, db: Session):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user