import hashlib

from DTOs.book_dto import BookDto
from DB.models import Book


def md5_file_decsr(f) -> str:
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5(fname) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_book_dto(book: Book) -> BookDto:
    with open(book.bookfile.path, "rb") as content:
        return BookDto(id=book.id,
                       title=book.title,
                       last_read_page=book.last_read_page,
                       content=content.read())

# TODO связь между sqlalchemy & pydantic
