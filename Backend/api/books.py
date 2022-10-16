import pathlib
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, APIRouter, Depends

import utils
from DTOs.bookmarkdto import BookmarkDto
from DB.BookMarkRepo import BookMarkRepo
from DTOs.book_dto import BookDtoObsolete, BookDto

from DB.models import User, Book
from services import Services, get_services

# from main import Services

# from . import router
# import logging
# import mimetypes

DIR = pathlib.Path(__file__).parent.parent.resolve()
book_router = APIRouter(prefix="/api")


# book_router = APIRouter()


@book_router.post('/books')
async def upload_file(request: Request, files: List[UploadFile] = File(...),
                      services: Services = Depends(get_services)):
    recv_file = files[0]
    file_hash = utils.md5_file_decsr(recv_file.file)
    existed = services.book_repo.get_book_file_by_hash(file_hash)
    if existed:
        bf = existed
    else:
        out_file_path = await utils.save_to_file_storage(recv_file)
        bf = services.book_repo.create_book_file(path=out_file_path, bf_hash=file_hash)
    user = services.user_repo.get_default_user()  # TODO get from request
    created = services.book_repo.add_book(bf, user=user, title=recv_file.filename)
    return utils.get_book_dto(created)


@book_router.get("/books", response_model=List[BookDto])
async def get_books(request: Request, services: Services = Depends(get_services)):
    user = services.user_repo.get_default_user()  # TODO get from request
    return list(map(utils.get_book_dto, services.book_repo.get_books_by_user(user)))


@book_router.get("/books/{book_id}", response_model=BookDtoObsolete)
async def get_book_by_id(book_id, services: Services = Depends(get_services)):
    b: Book = services.book_repo.get_book_by_id(book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return utils.get_book_dto(b)


@book_router.get("/books/{book_id}/bookmarks", response_model=List[BookmarkDto])
async def get_bookmarks_by_book(book_id, services: Services = Depends(get_services)):
    book: Book = services.book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return services.bookmark_repo.get_bookmarks_by_book(book)


@book_router.post("/books/{book_id}/bookmarks", response_model=BookmarkDto)
async def get_bookmarks_by_book(book_id: int, bm: BookmarkDto, services: Services = Depends(get_services)):
    book: Book = services.book_repo.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return services.bookmark_repo.create_bookmark(bm.quote, bm.comment, book)
