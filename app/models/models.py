# models/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

Base = declarative_base()
kst = pytz.timezone('Asia/Seoul')

# 다대다 관계를 위한 중간 테이블 정의
article_categories = Table(
    'article_categories',
    Base.metadata,
    Column('article_id', Integer, ForeignKey("articles.id"), primary_key=True),
    Column('category_id', Integer, ForeignKey("categories.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.now(kst), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(kst), nullable=True)

    articles = relationship("Article", back_populates="user")

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(kst), nullable=False)
    updated_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="articles")
    # 일대다 관계: 한 게시글은 여러 댓글을 가질 수 있음
    comments = relationship("Comment", back_populates="article")
    # 다대다 관계: 한 게시글은 여러 카테고리에 속할 수 있음
    categories = relationship("Category", secondary=article_categories, back_populates="articles")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(kst), nullable=False)
    updated_at = Column(DateTime, nullable=True)

    # 댓글과 게시글 간의 일대다 관계 반대편
    article = relationship("Article", back_populates="comments")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now(kst), nullable=False)
    updated_at = Column(DateTime, nullable=True)

    # 다대다 관계: 한 카테고리는 여러 게시글에 속할 수 있음
    articles = relationship("Article", secondary=article_categories, back_populates="categories")