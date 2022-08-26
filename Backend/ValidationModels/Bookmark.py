from pydantic import BaseModel
from typing import List

from ValidationModels.Book import Book


class Bookmark(BaseModel):
    book: Book
    quote: str
    comment: str
    tags: List[str] = []
