from sqlalchemy.orm.session import Session
from typing import Optional, List
from DB.models import User, BookFile, Book


class BookRepo:
    def __init__(self, s: Session):
        self.s = s

    def create_book_file(self, path: str, bf_hash: str) -> BookFile:
        # existed = self.get_book_file_by_hash(bf_hash)
        # if existed:
        #     return existed
        bf = BookFile(path=path, file_hash=bf_hash)
        self.s.add(bf)
        # book = Book(user_id=user.id, bookfile_id=bf.id)
        # self.s.add(book)
        self.s.commit()
        return bf

    def add_book(self, bf: BookFile, user: User, title: str) -> Book:
        if not bf:
            raise Exception()
        book = Book(user=user, bookfile=bf, title=title)
        self.s.add(book)
        self.s.commit()  # TODO constraint: can add (bf, u) only once
        return book

    def get_book_file_by_hash(self, bf_hash: str) -> Optional[BookFile]:
        return self.s.query(BookFile).filter_by(file_hash=bf_hash).first()

    def get_books_by_user(self, user: User) -> List[Book]:
        return self.s.query(Book).filter_by(user=user).all()

    def get_book_by_id(self, book_id) -> Optional[Book]:
        return self.s.query(Book).filter_by(id=book_id).first()
