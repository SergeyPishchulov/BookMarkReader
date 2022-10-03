# import os
# import pathlib
# import random
# import shutil
# from typing import List
#
# import aiofiles as aiofiles
# from fastapi import FastAPI, UploadFile, File, HTTPException, Request, APIRouter
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from starlette import status
# from starlette.templating import Jinja2Templates
#
# import utils
# from DTOs.bookmarkdto import BookmarkDto
# from DB.BookMarkRepo import BookMarkRepo
# from DTOs.book_dto import BookDto, BookContentlessDto
#
# from DB.BookRepo import BookRepo
# from DB.UserRepo import UserRepo
# from DB.db import get_session
# from DB.models import User, Book
# from sqlalchemy.orm.session import Session
# import logging
# import mimetypes
#
# mimetypes.init()
# # uvicorn main:app --reload
#
#
# app = FastAPI()
# router = APIRouter(prefix="/api")
#
# # http://127.0.0.1:8000/static/index.html
#
# templates = Jinja2Templates(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend")
#
#
# @app.get("/", response_class=HTMLResponse)
# async def hello(request: Request):
#     return templates.TemplateResponse("index1.html", {"request": request})
#
#
# mimetypes.add_type('application/javascript', '.js')
#
# app.mount(f"/static", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend"),
#           name="static")
#
# app.mount(f"/reader",
#           StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/distTreinetic/sample"),
#           name="treinetic")
#
# app.mount(f"/FileStorage", StaticFiles(directory=f"{pathlib.Path(__file__).parent.resolve()}/FileStorage"),
#           name="FileStorage")
# # "GET /2/META-INF/container.xml HTTP/1.1" 404 Not Found
# # этот паренб думает что если обратиться на /2 то получишь epub файл
