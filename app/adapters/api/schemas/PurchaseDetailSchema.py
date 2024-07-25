from pydantic import BaseModel
from typing import List, Optional


class PurchaseDetailSchema(BaseModel):
    id: Optional[int] = None
    purchase_id: Optional[int]
    customer_id: int
    book_id: int
    quantity: int
    unit_price: Optional[float]

    class Config:
        orm_mode = True

class ListPurchaseDetailsSchema(BaseModel):
    purchase_details: List[PurchaseDetailSchema]

    class Config:
        orm_mode = True