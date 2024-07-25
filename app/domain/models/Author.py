
from sqlalchemy import Column, Integer, String, Text
# Import the shared Base
from .base import Base

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    nationality = Column(String(100), nullable=True)
    biography = Column(Text, nullable=True)