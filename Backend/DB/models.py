from sqlalchemy import Column, String, Integer, Date, ForeignKey, BigInteger, inspect
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# from Book import BookDto

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="user")  # Class name, back_ref_name from that class


class Book(Base):
    """Encapsulate relationship between Book-file and User"""
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, default="Unnamed book")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="books")
    bookmarks = relationship("Bookmark", back_populates="book")
    last_read_page = Column(Integer, default=0)
    bookfile_id = Column(Integer, ForeignKey("bookfile.id"))
    bookfile = relationship("BookFile", back_populates="books")


class BookFile(Base):
    __tablename__ = "bookfile"
    id = Column(Integer, primary_key=True)
    file_hash = Column(String, nullable=False)
    path = Column(String)
    books = relationship("Book", back_populates="bookfile")


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    quote = Column(String)
    comment = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Book", back_populates="bookmarks")
    tags = relationship("Tag", back_populates="bookmark")

    def __repr__(self):
        return self.quote


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)
    bookmark_id = Column(Integer, ForeignKey('bookmarks.id'))
    bookmark = relationship("Bookmark", back_populates="tags")
