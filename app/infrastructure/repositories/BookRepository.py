from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models.Book import Book
from app.domain.interfaces.IBookRepository import IBookRepository

class BookRepository(IBookRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, book: Book) -> Book:
        self.db_session.add(book)
        self.db_session.commit()
        self.db_session.refresh(book)
        return book

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.db_session.query(Book).filter(Book.id == book_id).first()

    def get_all(self) -> List[Book]:
        return self.db_session.query(Book).all()

    def update(self, book: Book) -> Book:
        existing_book = self.db_session.merge(book)
        self.db_session.commit()
        return existing_book

    def delete(self, book_id: int) -> None:
        book_to_delete = self.db_session.query(Book).filter(Book.id == book_id).first()
        if book_to_delete:
            self.db_session.delete(book_to_delete)
            self.db_session.commit()