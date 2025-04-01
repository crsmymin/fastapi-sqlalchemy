from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.schemas import user_schema
from app.models import models
from app.databases import get_db
from app.utils.utils import verify_password, create_access_token

router = APIRouter(
    prefix="/api",
    tags=["login"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_model=user_schema.Token)
def login(request: user_schema.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}