from sqlalchemy.orm import Session
from models import models
from datetime import datetime
import pytz

kst = pytz.timezone('Asia/Seoul')

def create_article_service(article_data: dict, db: Session):
  db_article = models.Article(**article_data)
  db.add(db_article)
  db.commit()
  db.refresh(db_article)
  return db_article

def get_article_service(article_id: int, db: Session):
  return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles_service(skip: int, limit: int, db: Session):
  return db.query(models.Article).offset(skip).limit(limit).all()

def update_article_service(article_id: int, update_data: dict, db: Session):
  db_article = get_article_service(article_id, db)
  if db_article is None:
    return None
  for key, value in update_data.items():
    setattr(db_article, key, value)
  db_article.updated_at = datetime.now(kst)
  db.commit()
  db.refresh(db_article)
  return db_article

def delete_article_service(article_id: int, db: Session):
  db_article = get_article_service(article_id, db)
  if db_article is None:
    return None
  db.delete(db_article)
  db.commit()
  return db_article