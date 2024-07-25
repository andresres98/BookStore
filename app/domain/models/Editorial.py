
from sqlalchemy import Column, Integer, String
from .base import Base


class Editorial(Base):
    __tablename__ = 'editorial'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)