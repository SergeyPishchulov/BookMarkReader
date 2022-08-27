from sqlalchemy.orm.session import Session
from typing import Optional
from DB.models import User, BookFile, Book


class BookRepo:
    def __init__(self, s: Session):
        self.s = s

    def create_book_file(self, path: str, bf_hash: int) -> BookFile:
        bf = BookFile(path=path, file_hash=bf_hash)
        self.s.add(bf)
        # book = Book(user_id=user.id, bookfile_id=bf.id)
        # self.s.add(book)
        self.s.commit()
        return bf

    def add_book(self, bf: BookFile, user: User):
        if not bf:
            raise Exception()
        self.s.add(Book(user=user, bookfile=bf))
        self.s.commit()  # TODO constraint: can add (bf, u) only once

    def get_book_file_by_hash(self, bf_hash: int) -> Optional[BookFile]:
        return self.s.query(BookFile).filter_by(file_hash=bf_hash).first()
