import uvicorn
from fastapi import FastAPI, APIRouter, Depends

from DB.BookMarkRepo import BookMarkRepo
from api.bookmarks import router as books_router, bookmark_router
from sqlalchemy.orm.session import Session
from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
import logging

from api.books import book_router
from services import Services

app = FastAPI()
app.include_router(bookmark_router)
app.include_router(book_router)

s: Session = get_session(need_recreate=0)
services = Services(s)

# app.include_router(router)
# app.include_router(books_router, dependencies=Depends(services))

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
