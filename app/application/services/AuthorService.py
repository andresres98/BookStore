from typing import Optional, List

from fastapi import HTTPException

from app.domain.interfaces.IAuthorRepository import IAuthorRepository
from app.domain.models.Author import Author
from app.adapters.api.schemas.AuthorSchema import AuthorSchema

class AuthorService:
    def __init__(self, author_repository: IAuthorRepository):
        self.author_repository = author_repository

    def add_author(self, author_schema: AuthorSchema) -> Author:
        author = Author(
            name=author_schema.name,
            nationality=author_schema.nationality,
            biography=author_schema.biography
        )
        return self.author_repository.add(author)

    def get_author_by_id(self, author_id: int) -> Optional[Author]:
        return self.author_repository.get_by_id(author_id)

    def get_all_authors(self) -> List[Author]:
        return self.author_repository.get_all()

    def update_author(self, author_id: int, author_schema: AuthorSchema) -> Author:
        existing_author = self.author_repository.get_by_id(author_id)
        if existing_author is None:
            raise ValueError("Author not found")
        existing_author.name = author_schema.name
        existing_author.nationality = author_schema.nationality
        existing_author.biography = author_schema.biography
        return self.author_repository.update(existing_author)

    def delete_author(self, author_id: int) -> None:
        existing_author = self.author_repository.get_by_id(author_id)
        if existing_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        self.author_repository.delete(author_id)