from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from datetime import datetime
import pytz

kst = pytz.timezone('Asia/Seoul')

def create_category_service(category_data: dict, db: Session):
    # Category 생성 시 작성자(created_by) 필드가 이미 입력되어 있다고 가정
    db_category = models.Category(**category_data)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category_service(category_id: int, db: Session):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

def get_categories_service(skip: int, limit: int, db: Session, name: str = None):
    if name:
        db_categories = db.query(models.Category).filter(models.Category.name == name).offset(skip).limit(limit).all()
    else:
        db_categories = db.query(models.Category).offset(skip).limit(limit).all()
    if not db_categories:
        raise HTTPException(status_code=404, detail="Categories not found")
    return db_categories

def update_category_service(category_id: int, update_data: dict, db: Session, current_user: dict):
    db_category = get_category_service(category_id, db)
    # 사용자 권한 검증: 현재 로그인한 사용자의 id와 카테고리의 생성자(created_by)가 일치해야 함
    if str(current_user["sub"]) != str(db_category.created_by):
        raise HTTPException(status_code=403, detail="You do not have permission to update this category")
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db_category.updated_at = datetime.now(kst)
    db_category.updated_by = current_user["sub"]
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category_service(category_id: int, db: Session, current_user: dict):
    db_category = get_category_service(category_id, db)
    # 사용자 권한 검증: 현재 로그인한 사용자의 id와 카테고리의 생성자(created_by)가 일치해야 함
    if str(current_user["sub"]) != str(db_category.created_by):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this category")
    db.delete(db_category)
    db.commit()
    return db_category

def get_articles_by_category_service(category_id: int, skip: int, limit: int, db: Session):
    # 다대다 관계이므로 Article과 Category를 join하여 조회
    db_articles = (
        db.query(models.Article)
        .join(models.Article.categories)
        .filter(models.Category.id == category_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not db_articles:
        raise HTTPException(status_code=404, detail="Articles not found")
    return db_articles