from typing import Union

from fastapi import FastAPI
from app.routers import articles, users, login, comments, categories

app = FastAPI(
    title="fastapi example",
    description="A simple blog application with FastAPI",
    version="0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)
app.include_router(categories.router)