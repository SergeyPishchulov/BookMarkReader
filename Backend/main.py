import os
import random
import shutil
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

import utils
from Bookmark import BookmarkDto
from DB.BookMarkRepo import BookMarkRepo
from ValidationModels.Book import BookDto

from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
from DB.models import User, Book
from sqlalchemy.orm.session import Session

app = FastAPI()
s: Session = get_session(need_recreate=False)
book_repo = BookRepo(s)
user_repo = UserRepo(s)
bookmark_repo = BookMarkRepo(s)
app.mount("/static", StaticFiles(directory="../Frontend"), name="static")


# http://127.0.0.1:8000/static/index.html

@app.get("/")
async def hello():
    return {"message": "Hello World"}


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
    b: Book = book_repo.get_book_by_id(book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    with open(b.bookfile.path, "rb") as content:
        return BookDto(id=b.id,
                       title=b.title,
                       last_read_page=b.last_read_page,
                       content=content.read())


@app.get("/books/{book_id}/bookmarks")
async def get_bookmarks_by_book(book_id):
    book: Book = book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return bookmark_repo.get_bookmarks_by_book(book)


@app.post("/books/{book_id}/bookmarks")
async def get_bookmarks_by_book(book_id: int, bm: BookmarkDto):
    book: Book = book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    bookmark_repo.create_bookmark(bm.quote, bm.comment, book)


#
# @app.get("/bookmarks")
# async def get_bookmarks():
#     book = Book(title="EOSL")
#     return {"bookmarks": [Bookmark(book=book, quote="", comment="")]}

#
# @app.post("/bookmarks/")
# async def create_bookmark(bookmark: Bookmark):
#     print("posted")
#     return bookmark


@app.get("/bookmarks/{book_mark_id}")
async def get_bookmark(book_mark_id):
    return {"bookmarks": [1, 2, 3]}
