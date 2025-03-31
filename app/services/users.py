# app/services/user_service.py
from sqlalchemy.orm import Session
from models import models
from utils.utils import hash_password

def create_user_service(user_data: dict, db: Session):
  # 중복 사용자 체크
  existing_user = db.query(models.User).filter(models.User.email == user_data.get("email")).first()
  if existing_user:
      return None, "Email already registered"
  
  hashed_pw = hash_password(user_data.get("password"))
  new_user = models.User(
      username=user_data.get("username"),
      email=user_data.get("email"),
      password=hashed_pw
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user, None

def get_user_service(user_id: int, db: Session):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_users_service(skip: int, limit: int, db: Session):
  return db.query(models.User).offset(skip).limit(limit).all()

def update_user_service(user_id: int, update_data: dict, db: Session):
  db_user = db.query(models.User).filter(models.User.id == user_id).first()
  if not db_user:
      return None
  # 비밀번호가 업데이트 대상에 있다면 해싱 처리
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
      return None
  db.delete(db_user)
  db.commit()
  return db_user