from typing import Optional, List

from sqlalchemy.orm import Session
from app.domain.models.Book_Category import BookCategory
from app.domain.interfaces.IBookCategoryRepository import IBookCategoryRepository

class BookCategoryRepository(IBookCategoryRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, book_category: BookCategory) -> BookCategory:
        self.db_session.add(book_category)
        self.db_session.commit()
        self.db_session.refresh(book_category)
        return book_category

    def get_by_id(self, book_category_id: int) -> Optional[BookCategory]:
        return self.db_session.query(BookCategory).filter(BookCategory.id == book_category_id).first()

    def get_all(self) -> List[BookCategory]:
        return self.db_session.query(BookCategory).all()

    def update(self, book_category: BookCategory) -> BookCategory:
        existing_book_category = self.db_session.merge(book_category)
        self.db_session.commit()
        return existing_book_category

    def delete(self, book_category_id: int) -> None:
        book_category_to_delete = self.db_session.query(BookCategory).filter(BookCategory.id == book_category_id).first()
        if book_category_to_delete:
            self.db_session.delete(book_category_to_delete)
            self.db_session.commit()