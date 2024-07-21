
# app/adapters/api/schemas/author_schema.py

from pydantic import BaseModel

class AuthorSchema(BaseModel):
    id: int
    name: str
    nationality: str | None = None
    biography: str | None = None

    class Config:
        orm_mode = True