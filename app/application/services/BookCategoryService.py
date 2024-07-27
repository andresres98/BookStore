
from typing import Optional, List

from fastapi import HTTPException

from app.domain.interfaces.IBookCategoryRepository import IBookCategoryRepository
from app.domain.models.Book_Category import BookCategory
from app.adapters.api.schemas.BookCategorySchema import BookCategorySchema

class BookCategoryService:
    def __init__(self, book_category_repository: IBookCategoryRepository):
        self.book_category_repository = book_category_repository

    def add_book_category(self, book_category_schema: BookCategorySchema) -> BookCategory:
        book_category = BookCategory(
            name=book_category_schema.name
        )
        return self.book_category_repository.add(book_category)

    def get_book_category_by_id(self, book_category_id: int) -> Optional[BookCategory]:
        return self.book_category_repository.get_by_id(book_category_id)

    def get_all_book_categories(self) -> List[BookCategory]:
        return self.book_category_repository.get_all()

    def update_book_category(self, book_category_schema: BookCategorySchema) -> BookCategory:
        existing_book_category = self.book_category_repository.get_by_id(book_category_schema.id)
        if existing_book_category is None:
            raise ValueError("BookCategory not found")
        existing_book_category.name = book_category_schema.name
        return self.book_category_repository.update(existing_book_category)

    def delete_book_category(self, book_category_id: int) -> None:
        existing_book_category = self.book_category_repository.get_by_id(book_category_id)
        if existing_book_category is None:
            raise HTTPException(status_code=404, detail=f"BookCategory with ID {book_category_id} not found")

        self.book_category_repository.delete(book_category_id)