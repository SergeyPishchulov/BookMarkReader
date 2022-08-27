import os
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
from DB.models import User
from ValidationModels.Book import Book
from ValidationModels.Bookmark import Bookmark
from sqlalchemy.orm.session import Session

app = FastAPI()
s: Session = get_session()
book_repo = BookRepo(s)
user_repo = UserRepo(s)
app.mount("/static", StaticFiles(directory="../Frontend"), name="static")


# http://127.0.0.1:8000/static/index.html

@app.get("/")
async def hello():
    return {"message": "Hello World"}
    # with open('data.txt', 'r') as file:
    #     data = file.read('../')
    #     return HTMLResponse(content=)


@app.post('/upload')
def upload_file(files: List[UploadFile] = File(...)):
    file = files[0]
    file_hash = hash(file.file)  # TODO this hash depends on request. make hash dependent only from file content
    bf = book_repo.get_book_file_by_hash(file_hash)
    if not bf:
        path = f"FileStorage/{file_hash}{file.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            bf = book_repo.create_book_file(path=path, bf_hash=file_hash)
    user = user_repo.get_default_user()  # TODO get from request
    book_repo.add_book(bf, user=user)
    print('book saved')


@app.get("/bookmarks")
async def get_bookmarks():
    book = Book(title="EOSL")
    return {"bookmarks": [Bookmark(book=book, quote="", comment="")]}


@app.post("/bookmarks/")
async def create_bookmark(bookmark: Bookmark):
    print("posted")
    return bookmark


@app.get("/bookmarks/{book_mark_id}")
async def get_bookmark(book_mark_id):
    return {"bookmarks": [1, 2, 3]}
