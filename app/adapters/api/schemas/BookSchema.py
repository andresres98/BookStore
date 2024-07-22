from pydantic import BaseModel
from typing import Optional
from .EditorialSchema import EditorialSchema
from .BookCategorySchema import BookCategorySchema
from .AuthorSchema import AuthorSchema

class BookSchema(BaseModel):
    id: Optional[int] = None
    title: str
    author_id: Optional[int] = None
    isbn: Optional[str] = None
    price: float
    available_quantity: int
    category_id: Optional[int] = None
    editorial_id: Optional[int] = None
    author: Optional[AuthorSchema] = None
    category: Optional[BookCategorySchema] = None
    editorial: Optional[EditorialSchema] = None

    class Config:
        orm_mode = True