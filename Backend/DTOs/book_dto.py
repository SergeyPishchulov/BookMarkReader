from pydantic import BaseModel


class BookDto(BaseModel):
    id: int
    title: str
    last_read_page: int
    content: str


