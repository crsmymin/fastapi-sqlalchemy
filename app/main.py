from typing import Union

from fastapi import FastAPI
from routers import articles, users

app = FastAPI()

app.include_router(articles.router)
app.include_router(users.router)