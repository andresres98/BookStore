from typing import Optional
from pydantic import BaseModel, conint

class ReviewSchema(BaseModel):
    id: Optional[int] = None
    book_id: int
    customer_id: int
    rating: conint(ge=1, le=5)
    comment: Optional[str] = None

    class Config:
        orm_mode = True