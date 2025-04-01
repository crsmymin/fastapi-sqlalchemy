from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models import models
from datetime import datetime
import pytz

kst = pytz.timezone('Asia/Seoul')

def create_article_service(article_data: dict, db: Session):
    # 카테고리 ID 목록 추출 (없으면 빈 리스트로)
    category_ids = article_data.pop("category_ids", [])
    db_article = models.Article(**article_data)
    if category_ids:
        # DB에서 해당 카테고리 객체들을 조회
        categories = db.query(models.Category).filter(models.Category.id.in_(category_ids)).all()
        if not categories:
            raise HTTPException(status_code=404, detail="No valid categories found")
        # Article의 다대다 관계에 할당
        db_article.categories = categories
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article_service(article_id: int, db: Session):
    # Article과 연관 댓글을 미리 로드하여 조회
    db_article = (
        db.query(models.Article)
            .options(
                joinedload(models.Article.comments),
                joinedload(models.Article.categories)
            )
            .filter(models.Article.id == article_id)
            .first()    
    )
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

def get_articles_service(skip: int, limit: int, db: Session):
    return db.query(models.Article).options(joinedload(models.Article.categories)).offset(skip).limit(limit).all()

def update_article_service(article_id: int, update_data: dict, db: Session, current_user: dict):
    category_ids = update_data.pop("category_ids", [])
    db_article = get_article_service(article_id, db)  # 존재하지 않으면 HTTPException 발생
    if category_ids:
        # DB에서 해당 카테고리 객체들을 조회
        categories = db.query(models.Category).filter(models.Category.id.in_(category_ids)).all()
        if not categories:
            raise HTTPException(status_code=404, detail="No valid categories found")
        # Article의 다대다 관계에 할당
        db_article.categories = categories
    # 사용자 권한 검증: 현재 로그인 사용자의 id와 작성자 id가 일치해야 함
    if str(current_user["sub"]) != str(db_article.user_id):
        raise HTTPException(status_code=403, detail="You do not have permission to update this article")
    
    for key, value in update_data.items():
        setattr(db_article, key, value)
    db_article.updated_at = datetime.now(kst)
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article_service(article_id: int, db: Session, current_user: dict):
    db_article = get_article_service(article_id, db)  # 존재하지 않으면 HTTPException 발생
    # 사용자 권한 검증: 현재 로그인 사용자의 id와 작성자 id가 일치해야 함
    if str(current_user["sub"]) != str(db_article.user_id):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this article")
    db.delete(db_article)
    db.commit()
    return db_article