from typing import Optional

from pydantic import BaseModel

class EditorialSchema(BaseModel):
    id: Optional[int] = None
    name: str
    address: str | None = None
    country: str | None = None

    class Config:
        orm_mode = True