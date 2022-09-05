import os
import pathlib
import random
import shutil
from typing import List

import aiofiles as aiofiles
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette import status

import utils
from DTOs.bookmarkdto import BookmarkDto
from DB.BookMarkRepo import BookMarkRepo
from DTOs.book_dto import BookDto, BookContentlessDto

from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
from DB.models import User, Book
from sqlalchemy.orm.session import Session
import logging
import mimetypes

mimetypes.init()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
# fh = logging.FileHandler(filename='./Logs/server.log', mode='w')  # DELETE in the begining
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

ch.setFormatter(formatter)
# fh.setFormatter(formatter)
logger.addHandler(ch)  # Exporting logs to the screen
# logger.addHandler(fh)  # Exporting logs to a file

DIR = pathlib.Path(__file__).parent.resolve()
app = FastAPI()


# http://127.0.0.1:8000/static/index.html


# @app.middleware("http")
# async def request_middleware(request, call_next):
#     # debug("Request started")
#
#     try:
#         return await call_next(request)
#
#     except Exception as ex:
#         logger.debug(f"Request failed: {ex}")
#         raise HTTPException(status_code=505)
#         # return JSONResponse(content={"success": False}, status_code=500)
#
#     # finally:
#     #     assert request_id_contextvar.get() == request_id
#     #     debug("Request ended")


@app.get("/")
async def hello():
    logger.info("Hello=")
    return {"message": "Hello World"}


@app.post('/books')
async def upload_file(request: Request, files: List[UploadFile] = File(...)) -> BookDto:
    # logger.info(request)
    recv_file = files[0]
    file_hash = utils.md5_file_decsr(recv_file.file)
    print(file_hash)
    logger.debug(file_hash)
    existed = book_repo.get_book_file_by_hash(file_hash)
    if existed:
        bf = existed
    else:
        out_file_path = f"{DIR}/FileStorage/{random.randint(10 ** 8, 10 ** 9)}{recv_file.filename}"
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            await recv_file.seek(0)
            while content := await recv_file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk
        recv_file.file.close()
        bf = book_repo.create_book_file(path=out_file_path, bf_hash=file_hash)
    user = user_repo.get_default_user()  # TODO get from request
    created = book_repo.add_book(bf, user=user)
    print('book saved')
    return utils.get_book_dto(created)


@app.get("/books", response_model=List[BookContentlessDto])
async def get_books(request: Request):
    # logger.info(request)
    user = user_repo.get_default_user()  # TODO get from request
    return book_repo.get_books_by_user(user)


@app.get("/books/{book_id}", response_model=BookDto)
async def get_book_by_id(book_id):
    b: Book = book_repo.get_book_by_id(book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return utils.get_book_dto(b)


@app.get("/books/{book_id}/bookmarks", response_model=List[BookmarkDto])
async def get_bookmarks_by_book(book_id):
    book: Book = book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return bookmark_repo.get_bookmarks_by_book(book)


@app.post("/books/{book_id}/bookmarks", response_model=BookmarkDto)
async def get_bookmarks_by_book(book_id: int, bm: BookmarkDto):
    print("posted bookmark")
    book: Book = book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return bookmark_repo.create_bookmark(bm.quote, bm.comment, book)


@app.get("/bookmarks", response_model=List[BookmarkDto])
async def get_bookmarks():
    user = user_repo.get_default_user()
    bkmks_orms = bookmark_repo.get_bookmarks_by_user(user)
    # print(bkmks_orms[0])
    return bkmks_orms
    # return [BookmarkDto.from_orm(x) for x in bkmks_orms]


mimetypes.add_type('application/javascript', '.js')

s: Session = get_session(need_recreate=1)
book_repo = BookRepo(s)
user_repo = UserRepo(s)
bookmark_repo = BookMarkRepo(s)
app.mount(f"/static", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend"),
          name="static")

app.mount(f"/treinetic", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/distTreinetic"),
          name="treinetic")
