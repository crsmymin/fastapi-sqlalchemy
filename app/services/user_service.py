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

def get_user_service(user_id: int, db: Session, current_user: dict):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    print(f"Current user: {current_user['sub']}")
    print(f"DB user: {db_user.id}")
    # 사용자 정보가 존재하지 않을 경우
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # 현재 사용자가 admin이거나, 요청한 사용자의 ID와 일치하는 경우
    # admin은 모든 사용자 정보에 접근 가능
    # 일반 사용자는 자신의 정보만 접근 가능
    if current_user["role"] == "admin" or str(current_user["sub"]) == str(db_user.id):
        return db_user
    else:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")

def get_users_service(skip: int, limit: int, search_word: str, db: Session):
    print(search_word)
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_service(user_id: int, update_data: dict, db: Session, current_user: dict):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    # 사용자 정보가 존재하지 않을 경우
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # 현재 사용자가 admin이거나, 요청한 사용자의 ID와 일치하는 경우
    # admin은 모든 사용자 정보 수정 가능
    # 일반 사용자는 자신의 정보만 수정 가능
    if current_user["role"] == "admin" or str(current_user["sub"]) == str(db_user.id):
        pass
    else:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    # 비밀번호 업데이트 시 해싱 처리
    if "password" in update_data and update_data["password"]:
        update_data["password"] = hash_password(update_data["password"])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_service(user_id: int, db: Session, current_user: dict):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    # 사용자 정보가 존재하지 않을 경우
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # 현재 사용자가 admin이거나, 요청한 사용자의 ID와 일치하는 경우
    # admin은 모든 사용자 삭제 가능
    # 일반 사용자는 자신의 정보만 삭제 가능
    if current_user["role"] == "admin" or str(current_user["sub"]) == str(db_user.id):
        pass
    else:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    # 사용자 삭제
    db.delete(db_user)
    db.commit()
    return db_user