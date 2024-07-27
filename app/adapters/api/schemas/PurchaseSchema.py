from pydantic import BaseModel
from typing import Optional, List
from datetime import date

from app.adapters.api.schemas.CustomerSchema import CustomerSchema
from app.domain.models.Purchase_Detail import Purchase_Detail


class PurchaseSchema(BaseModel):
    id: Optional[int] = None
    customer_id: int = None
    date: date
    total_amount: Optional[float] = None
    customer: Optional[CustomerSchema] = None

    class Config:
        orm_mode = True