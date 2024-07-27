from typing import Optional
from pydantic import BaseModel, conint

from app.adapters.api.schemas.BookSchema import BookSchema
from app.adapters.api.schemas.CustomerSchema import CustomerSchema


class ReviewSchema(BaseModel):
    id: Optional[int] = None
    book_id: int
    customer_id: int
    rating: conint(ge=1, le=5)
    comment: Optional[str] = None
    book: Optional[BookSchema] = None
    customer: Optional[CustomerSchema] = None

    class Config:
        orm_mode = True