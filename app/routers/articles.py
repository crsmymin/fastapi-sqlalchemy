from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import article_schema
from app.services import article_service
from app.utils.utils import get_current_user
from app.databases import get_db
from typing import List

router = APIRouter(
    prefix="/api",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/articles/", response_model=article_schema.ArticleResponse)
def create_article(
    article: article_schema.ArticleCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    article_data = article.model_dump()
    article_data["user_id"] = current_user["sub"]
    return article_service.create_article_service(article_data, db)

@router.get("/articles/{article_id}", response_model=article_schema.ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
    return article_service.get_article_service(article_id, db)

@router.get("/articles/", response_model=List[article_schema.ArticleResponse])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return article_service.get_articles_service(skip, limit, db)

@router.put("/articles/{article_id}", response_model=article_schema.ArticleResponse)
def update_article(
    article_id: int, 
    article: article_schema.ArticleUpdate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    update_data = article.model_dump(exclude_unset=True)
    return article_service.update_article_service(article_id, update_data, db, current_user)

@router.delete("/articles/{article_id}", response_model=article_schema.ArticleResponse)
def delete_article(
    article_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return article_service.delete_article_service(article_id, db, current_user)