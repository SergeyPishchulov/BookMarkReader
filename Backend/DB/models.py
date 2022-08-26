from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    books = relationship("Book", back_populates="user")  # Class name, back_ref_name from that class


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="books")
    bookmarks = relationship("Bookmark", back_populates="book")


class Bookmark(Base):
    __tablename__ = 'bookmarks'
    id = Column(Integer, primary_key=True)
    quote = Column(String)
    comment = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Book", back_populates="bookmarks")
    tags = relationship("Tag", back_populates="bookmark")


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String, nullable=False)
    bookmark_id = Column(Integer, ForeignKey('bookmarks.id'))
    bookmark = relationship("Bookmark", back_populates="tags")
