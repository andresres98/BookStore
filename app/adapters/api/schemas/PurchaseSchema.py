from pydantic import BaseModel
from typing import Optional
from datetime import date

class PurchaseSchema(BaseModel):
    id: Optional[int] = None
    customer_id: int = None
    date: Optional[date] = None
    total_amount: Optional[float] = None

    class Config:
        orm_mode = True