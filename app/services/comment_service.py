from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from datetime import datetime
import pytz

kst = pytz.timezone('Asia/Seoul')

def create_comment_service(comment_data: dict, db: Session):
    # 입력받은 article_id에 해당하는 Article이 존재하는지 검증
    db_article = db.query(models.Article).filter(models.Article.id == comment_data["article_id"]).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # 댓글 생성
    db_comment = models.Comment(**comment_data)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment_service(comment_id: int, db: Session):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

def get_comments_service(skip: int, limit: int, user_id: int, article_id: int, db: Session):
    if(user_id != None and article_id != None):
        db_comments = db.query(models.Comment).filter(models.Comment.user_id == user_id, models.Comment.article_id == article_id).offset(skip).limit(limit).all()
    elif(user_id != None):
        db_comments = db.query(models.Comment).filter(models.Comment.user_id == user_id).offset(skip).limit(limit).all()
    elif(article_id != None):
        db_comments = db.query(models.Comment).filter(models.Comment.article_id == article_id).offset(skip).limit(limit).all()
    else:
        db_comments = db.query(models.Comment).offset(skip).limit(limit).all()
    if not db_comments:
        raise HTTPException(status_code=404, detail="Comments not found")
    return db_comments

def update_comment_service(comment_id: int, update_data: dict, db: Session, current_user: dict):
    db_comment = get_comment_service(comment_id, db)
    # 사용자 권한 검증: 현재 로그인한 사용자와 댓글 작성자가 동일한지 확인
    if str(current_user["sub"]) != str(db_comment.user_id):
        raise HTTPException(status_code=403, detail="You do not have permission to update this comment")
    # article_id는 댓글 작성시 입력받은 article_id와 동일해야 함
    if db_comment.article_id != update_data["article_id"]:
        raise HTTPException(status_code=403, detail="You cannot change the article_id of this comment")
    for key, value in update_data.items():
        setattr(db_comment, key, value)
    db_comment.updated_at = datetime.now(kst)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment_service(comment_id: int, db: Session, current_user: dict):
    db_comment = get_comment_service(comment_id, db)
    # 사용자 권한 검증: 현재 로그인한 사용자와 댓글 작성자가 동일한지 확인
    if str(current_user["sub"]) != str(db_comment.user_id):
        raise HTTPException(status_code=403, detail="You do not have permission to delete this comment")
    db.delete(db_comment)
    db.commit()
    return db_comment