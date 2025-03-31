# app/utils/utils.py
import os
import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import pytz

load_dotenv()
kst = pytz.timezone('Asia/Seoul')

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 180))
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def get_current_user(token: str = Depends(oauth2_scheme)):
  """ 
  헤더에서 토큰을 추출하고, 토큰을 해독하여 사용자 정보를 반환 
  """
  if token is None:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid authentication credentials",
          headers={"WWW-Authenticate": "Bearer"},
      )
  # "Bearer " 접두사가 있다면 먼저 제거
  if token.startswith("Bearer "):
      token = token[len("Bearer "):]
  payload = decode_access_token(token)
  return payload

def hash_password(password: str) -> str:
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
  return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
  to_encode = data.copy()
  expire = datetime.now(kst) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def decode_access_token(token: str) -> dict:
  try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      return payload
  except jwt.ExpiredSignatureError:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Token has expired",
          headers={"WWW-Authenticate": "Bearer"},
      )
  except JWTError:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid token",
          headers={"WWW-Authenticate": "Bearer"},
      )