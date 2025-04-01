from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import category_schema, article_schema
from app.services import category_service
from app.utils.utils import get_current_user
from app.databases import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/api",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

@router.post("/categories/", response_model=category_schema.CategoryResponse)
def create_category(
    category: category_schema.CategoryCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    category_data = category.model_dump()
    # 모델의 작성자 필드는 created_by로 정의되어 있으므로 설정
    category_data["created_by"] = current_user["sub"]
    return category_service.create_category_service(category_data, db)

@router.get("/categories/{category_id}", response_model=category_schema.CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category_service(category_id, db)

@router.get("/categories/", response_model=List[category_schema.CategoryResponse])
def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    name: Optional[str] = None
):
    return category_service.get_categories_service(skip, limit, db, name)

@router.put("/categories/{category_id}", response_model=category_schema.CategoryResponse)
def update_category(
    category_id: int, 
    category: category_schema.CategoryUpdate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    update_data = category.model_dump(exclude_unset=True)
    return category_service.update_category_service(category_id, update_data, db, current_user)

@router.delete("/categories/{category_id}", response_model=category_schema.CategoryResponse)
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    return category_service.delete_category_service(category_id, db, current_user)

@router.get("/categories/{category_id}/articles", response_model=List[article_schema.ArticlesResponse])
def read_articles_by_category(
    category_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return category_service.get_articles_by_category_service(category_id, skip, limit, db)