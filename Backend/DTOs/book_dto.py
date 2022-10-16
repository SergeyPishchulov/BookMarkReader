from pydantic import BaseModel


class BookDto(BaseModel):
    id: int
    title: str
    last_read_page: int
    file_url: str

    class Config:
        orm_mode = True


class BookDtoObsolete(BookDto):
    content: str = None

    class Config:
        orm_mode = True
