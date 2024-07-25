
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .Book_Category import BookCategory
from .Author import Author
from .Editorial import Editorial

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    isbn = Column(String(20))
    price = Column(DECIMAL(10, 2), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('bookcategory.id'))
    editorial_id = Column(Integer, ForeignKey('editorial.id'))

    author = relationship(Author)
    category = relationship(BookCategory)
    editorial = relationship(Editorial)