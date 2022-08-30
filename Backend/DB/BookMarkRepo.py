from sqlalchemy.orm.session import Session
from typing import Optional, List
from DB.models import User, BookFile, Book, Bookmark


class BookMarkRepo:
    def __init__(self, s: Session):
        self.s = s

    def get_bookmarks_by_book(self, book: Book) -> List[Bookmark]:
        return self.s.query(Bookmark).filter_by(book=book).all()

    def create_bookmark(self, quote: str, comment: str, book: Book) -> Bookmark:
        bm = Bookmark(quote=quote, comment=comment, book=book)
        self.s.add(bm)
        self.s.commit()
        return bm

# def create_book_file(self, path: str, bf_hash: str) -> BookFile:
#     # existed = self.get_book_file_by_hash(bf_hash)
#     # if existed:
#     #     return existed
#     bf = BookFile(path=path, file_hash=bf_hash)
#     self.s.add(bf)
#     # book = Book(user_id=user.id, bookfile_id=bf.id)
#     # self.s.add(book)
#     self.s.commit()
#     return bf
#
# def add_book(self, bf: BookFile, user: User):
#     if not bf:
#         raise Exception()
#     self.s.add(Book(user=user, bookfile=bf))
#     self.s.commit()  # TODO constraint: can add (bf, u) only once
#
# def get_book_file_by_hash(self, bf_hash: str) -> Optional[BookFile]:
#     return self.s.query(BookFile).filter_by(file_hash=bf_hash).first()
#
# def get_books_by_user(self, user: User) -> List[Book]:
#     return self.s.query(Book).filter_by(user=user).all()
#
# def get_book_by_id(self, book_id) -> Optional[Book]:
#     return self.s.query(Book).filter_by(id=book_id).first()
