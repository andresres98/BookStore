
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

class BookCategory(Base):
    __tablename__ = 'bookcategory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)