from pydantic import BaseModel


class BookContentlessDto(BaseModel):
    id: int
    title: str
    last_read_page: int

    class Config:
        orm_mode = True


class BookDto(BookContentlessDto):
    content: str = None

    class Config:
        orm_mode = True
