from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship

from .Customer import Customer
from .base import Base

class Purchase(Base):
    __tablename__ = 'purchase'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date = Column(Date, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    customer = relationship(Customer)