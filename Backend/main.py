from functools import lru_cache

import uvicorn
from fastapi import FastAPI, APIRouter, Depends

from DB.BookMarkRepo import BookMarkRepo
from api.bookmarks import bookmark_router
from sqlalchemy.orm.session import Session
from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
import logging

from api.books import book_router
from services import Services, get_services

app = FastAPI()
# app.include_router(bookmark_router)
# app.include_router(book_router)
#


services = get_services()

app.include_router(book_router)
app.include_router(bookmark_router)
# app.include_router(books_router, dependencies=Depends(services))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
