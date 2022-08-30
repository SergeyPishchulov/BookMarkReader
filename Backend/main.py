import os
import random
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import utils
from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
from DB.models import User
from ValidationModels.Book import Book
from ValidationModels.Bookmark import Bookmark
from sqlalchemy.orm.session import Session

app = FastAPI()
s: Session = get_session(need_recreate=False)
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
    tmp_path = f"FileStorage/{random.randint(10 ** 8, 10 ** 9)}{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_hash = utils.md5(tmp_path)
    existed = book_repo.get_book_file_by_hash(file_hash)
    if existed:
        bf = existed
        os.remove(tmp_path)
    else:
        bf = book_repo.create_book_file(path=tmp_path, bf_hash=file_hash)
    user = user_repo.get_default_user()  # TODO get from request
    book_repo.add_book(bf, user=user)
    print('book saved')
    # TODO tests: same file with different names, same names with different files


@app.get("/books")
async def get_books():
    user = user_repo.get_default_user()  # TODO get from request
    return book_repo.get_books_by_user(user)


@app.get("/books/{book_id}")
async def get_book_by_id(book_id):
    return book_repo.get_book_by_id(book_id)


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
