from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import article
from app.utils.utils import get_current_user
from app.databases import get_db
from typing import List
from app.services import articles

router = APIRouter(
	prefix="/api",
	tags=["articles"],
	responses={404: {"description": "Not found"}},
)

@router.post("/articles/", response_model=article.ArticleResponse)
def create_article(article: article.ArticleCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
	article_data = article.model_dump()
	article_data["user_id"] = current_user["sub"]
	return articles.create_article_service(article_data, db)

@router.get("/articles/{article_id}", response_model=article.ArticleResponse)
def read_article(article_id: int, db: Session = Depends(get_db)):
	db_article = articles.get_article_service(article_id, db)
	if db_article is None:
			raise HTTPException(status_code=404, detail="Article not found")
	return db_article

@router.get("/articles/", response_model=List[article.ArticleResponse])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return articles.get_articles_service(skip, limit, db)

@router.put("/articles/{article_id}", response_model=article.ArticleResponse)
def update_article(article_id: int, article: article.ArticleUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
	db_article = articles.get_article_service(article_id, db)
	
	if db_article is None:
			raise HTTPException(status_code=404, detail="Article not found")
	
	# 사용자 권한 확인
	if str(current_user["sub"]) != str(db_article.user_id):
			raise HTTPException(status_code=403, detail="You do not have permission to update this article")
	
	update_data = article.model_dump(exclude_unset=True)
	updated_article = articles.update_article_service(article_id, update_data, db)
	return updated_article

@router.delete("/articles/{article_id}", response_model=article.ArticleResponse)
def delete_article(article_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
	db_article = articles.get_article_service(article_id, db)
	
	if db_article is None:
			raise HTTPException(status_code=404, detail="Article not found")
	
	# 사용자 권한 확인
	if str(current_user["sub"]) != str(db_article.user_id):
			raise HTTPException(status_code=403, detail="You do not have permission to delete this article")
	
	deleted_article = articles.delete_article_service(article_id, db)
	return deleted_article