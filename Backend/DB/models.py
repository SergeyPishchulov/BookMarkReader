from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    books = relationship("Book", back_populates="user")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="books")

# class Bookmark(Base):
#     __tablename__ = 'bookmarks'
#     id = Column(Integer, primary_key=True)
#     quote = Column(String)
#     comment = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
# user = relationship("users", back_populates="bookmarks")

# class Tag(Base):
#     __tablename__ = 'tags'
#     id = Column(Integer, primary_key=True)
#     tag = Column(String, nullable=False)
#     bookmark_id = Column(Integer, ForeignKey('bookmarks.id'))
#     bookmark = relationship("bookmarks", back_populates="tags")


# Bookmark.tags = relationship("Tag", order_by=Tag.id, back_populates="bookmark")
# User.bookmarks = relationship("Bookmark", order_by=Bookmark.id, back_populates="user")
