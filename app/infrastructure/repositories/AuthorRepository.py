from typing import Optional, List

from sqlalchemy.orm import Session
from app.domain.models.Author import Author
from app.domain.interfaces.IAuthorRepository import IAuthorRepository

class AuthorRepository(IAuthorRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, author: Author) -> Author:
        self.db_session.add(author)
        self.db_session.commit()
        self.db_session.refresh(author)
        return author

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return self.db_session.query(Author).filter(Author.id == author_id).first()

    def get_all(self) -> List[Author]:
        return self.db_session.query(Author).all()

    def update(self, author: Author) -> Author:
        existing_author = self.db_session.merge(author)
        self.db_session.commit()
        return existing_author

    def delete(self, author_id: int) -> None:
        author_to_delete = self.db_session.query(Author).filter(Author.id == author_id).first()
        if author_to_delete:
            self.db_session.delete(author_to_delete)
            self.db_session.commit()