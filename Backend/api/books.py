import os
import pathlib
import random
import shutil
from typing import List

import aiofiles as aiofiles
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.templating import Jinja2Templates

import utils
from DTOs.bookmarkdto import BookmarkDto
from DB.BookMarkRepo import BookMarkRepo
from DTOs.book_dto import BookDto, BookContentlessDto

from DB.models import User, Book
# from main import Services

from . import router
import logging
import mimetypes

DIR = pathlib.Path(__file__).parent.parent.resolve()
book_router = APIRouter()


# @router.post('/books')
# async def upload_file(request: Request, files: List[UploadFile] = File(...),
#                       services: Services = Depends(Services)):
#     # logger.info(request)
#     recv_file = files[0]
#     file_hash = utils.md5_file_decsr(recv_file.file)
#     print(file_hash)
#     services.logger.debug(file_hash)
#     existed = services.book_repo.get_book_file_by_hash(file_hash)
#     if existed:
#         bf = existed
#     else:
#         out_file_path = f"/FileStorage/{random.randint(10 ** 8, 10 ** 9)}{recv_file.filename}"
#         full_path = str(DIR) + out_file_path
#         async with aiofiles.open(full_path, 'wb') as out_file:
#             await recv_file.seek(0)
#             while content := await recv_file.read(1024):  # async read chunk
#                 await out_file.write(content)  # async write chunk
#         recv_file.file.close()
#         bf = services.book_repo.create_book_file(path=out_file_path, bf_hash=file_hash)
#     user = services.user_repo.get_default_user()  # TODO get from request
#     created = services.book_repo.add_book(bf, user=user, title=recv_file.filename)
#     print('book saved')
#     return utils.get_book_dto(created)


@book_router.get("/books", response_model=List[BookContentlessDto])
async def get_books(request: Request):
    return 2
    # logger.info(request)
    user = services.user_repo.get_default_user()  # TODO get from request
    return services.book_repo.get_books_by_user(user)

# @router.get("/books/{book_id}", response_model=BookDto)
# async def get_book_by_id(book_id, services: Services = Depends(Services)):
#     b: Book = services.book_repo.get_book_by_id(book_id)
#     if not b:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return utils.get_book_dto(b)
#
#
# @router.get("/books/{book_id}/bookmarks", response_model=List[BookmarkDto])
# async def get_bookmarks_by_book(book_id, services: Services = Depends(Services)):
#     book: Book = services.book_repo.get_book_by_id(book_id)
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return services.bookmark_repo.get_bookmarks_by_book(book)
#
#
# @router.post("/books/{book_id}/bookmarks", response_model=BookmarkDto)
# async def get_bookmarks_by_book(book_id: int, bm: BookmarkDto, services: Services = Depends(Services)):
#     print("posted bookmark")
#     book: Book = services.book_repo.get_book_by_id(book_id)
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return services.bookmark_repo.create_bookmark(bm.quote, bm.comment, book)
