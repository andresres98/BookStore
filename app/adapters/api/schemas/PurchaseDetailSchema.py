from pydantic import BaseModel
from typing import List, Optional

from app.adapters.api.schemas.BookSchema import BookSchema
from app.adapters.api.schemas.CustomerSchema import CustomerSchema


class PurchaseDetailSchema(BaseModel):
    id: Optional[int] = None
    purchase_id: Optional[int]
    customer_id: int
    book_id: int
    quantity: int
    unit_price: Optional[float]
    customer: Optional[CustomerSchema] = None
    book: Optional[BookSchema] = None

    class Config:
        orm_mode = True