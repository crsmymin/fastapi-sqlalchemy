# models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

Base = declarative_base()

kst = pytz.timezone('Asia/Seoul')

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(kst))
    created_at = Column(DateTime, default=datetime.now(kst))

    articles = relationship("Article", back_populates="user")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(String(255))
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.now(kst))
    created_at = Column(DateTime, default=datetime.now(kst))

    user = relationship("User", back_populates="articles")