
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'Book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    isbn = Column(String(20))
    price = Column(DECIMAL(10, 2), nullable=False)
    available_quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('Book_Category.id'))
    editorial_id = Column(Integer, ForeignKey('Editorial.id'))

    # Relationships
    author = relationship("Author")
    category = relationship("BookCategory")
    editorial = relationship("Editorial")