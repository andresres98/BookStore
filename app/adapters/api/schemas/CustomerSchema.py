from typing import Optional
from pydantic import BaseModel

class CustomerSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None

    class Config:
        orm_mode = True