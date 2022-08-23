from fastapi import FastAPI

from Models.Book import Book
from Models.Bookmark import Bookmark

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}


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
