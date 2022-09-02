from pydantic import BaseModel
from typing import List


class BookmarkDto(BaseModel):
    book_id: int
    quote: str
    comment: str
    tags: List[str] = []

    class Config:
        orm_mode = True
