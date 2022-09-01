from pydantic import BaseModel
from typing import List


class bookmark_dto(BaseModel):
    book_id: int
    quote: str
    comment: str
    tags: List[str] = []
