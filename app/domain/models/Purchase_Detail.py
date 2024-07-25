from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .Book import Book
from .Purchase import Purchase
from .base import Base

class Purchase_Detail(Base):
    __tablename__ = 'purchasedetail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_id = Column(Integer, ForeignKey('purchase.id'))
    customer_id = Column(Integer, nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    purchase = relationship(Purchase)
    book = relationship(Book)