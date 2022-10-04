import pathlib
from functools import lru_cache

import uvicorn
from fastapi import FastAPI, APIRouter, Depends, Request, responses, status
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from DB.BookMarkRepo import BookMarkRepo
from api.bookmarks import bookmark_router
from sqlalchemy.orm.session import Session
from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from DB.db import get_session
import logging

from api.books import book_router
from services import Services, get_services
import mimetypes

mimetypes.init()
app = FastAPI()
mimetypes.add_type('application/javascript', '.js')
#
# strongly_typed_templates = Jinja2Templates(
#     directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/static")
#
# reader_templates = Jinja2Templates(
#     directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/dist/sample")
services = get_services()

app.include_router(book_router)
app.include_router(bookmark_router)


# @app.get("/reader")
# async def reader(book_uri: str):
#     user = services.user_repo.get_default_user()
#     bkmks_orms = services.bookmark_repo.get_bookmarks_by_user(user)
#     # print(bkmks_orms[0])
#     return bkmks_orms


# @app.get("/reader", response_class=HTMLResponse)
# async def reader(request: Request):
#     return treinetic_templates.TemplateResponse("reader.html", {"request": request})
#
# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     return strongly_typed_templates.TemplateResponse("reader.html", {"request": request})


# @app.get("/reader", response_class=HTMLResponse)
# async def reader(request: Request):
#     return reader_templates.TemplateResponse("sample/reader.html", {"request": request})
@app.get("/")
async def index(request: Request):
    return responses.RedirectResponse(
        '/static/index.html',
        status_code=status.HTTP_302_FOUND)


# app.mount(f"/sample",
#           StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/distTreinetic_obsolete/sample"),
#           name="sample")
#

app.mount(f"/fs", StaticFiles(directory=f"{pathlib.Path(__file__).parent.resolve()}/FileStorage"),
          name="fs")
app.mount(f"/sample", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/dist/sample"),
          name="sample")
app.mount(f"/static", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/static"),
          name="static")
# app.mount(f"/", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/static"),
#           name="static")
# app.include_router(books_router, dependencies=Depends(services))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
