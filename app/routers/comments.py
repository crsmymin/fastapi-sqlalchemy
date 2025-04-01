from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import comment_schema
from app.services import comment_service
from app.utils.utils import get_current_user
from app.databases import get_db
from typing import List

router = APIRouter(
    prefix="/api",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/comments/", response_model=comment_schema.CommentResponse)
def create_comment(
    comment: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    comment_data = comment.model_dump()
    comment_data["user_id"] = current_user["sub"]
    return comment_service.create_comment_service(comment_data, db)

@router.get("/comments/{comment_id}", response_model=comment_schema.CommentResponse)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comment_service(comment_id, db)

@router.get("/comments/", response_model=List[comment_schema.CommentResponse])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return comment_service.get_comments_service(skip, limit, db)

@router.put("/comments/{comment_id}", response_model=comment_schema.CommentResponse)
def update_comment(
    comment_id: int,
    comment: comment_schema.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    update_data = comment.model_dump(exclude_unset=True)
    return comment_service.update_comment_service(comment_id, update_data, db, current_user)

@router.delete("/comments/{comment_id}", response_model=comment_schema.CommentResponse)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comment_service.delete_comment_service(comment_id, db, current_user)