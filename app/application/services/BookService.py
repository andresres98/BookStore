from typing import Optional, List

from fastapi import HTTPException

from app.domain.interfaces.IBookRepository import IBookRepository
from app.domain.models.Book import Book
from app.adapters.api.schemas.BookSchema import BookSchema

class BookService:
    def __init__(self, book_repository: IBookRepository):
        self.book_repository = book_repository

    def add_book(self, book_schema: BookSchema) -> Book:
        book = Book(
            title=book_schema.title,
            author_id=book_schema.author_id,
            isbn=book_schema.isbn,
            price=book_schema.price,
            available_quantity=book_schema.available_quantity,
            category_id=book_schema.category_id,
            editorial_id=book_schema.editorial_id
        )
        return self.book_repository.add(book)

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        return self.book_repository.get_by_id(book_id)

    def get_all_books(self) -> List[Book]:
        return self.book_repository.get_all()

    def update_book(self, book_id: int, book_schema: BookSchema) -> Book:
        existing_book = self.book_repository.get_by_id(book_id)
        if existing_book is None:
            raise ValueError("Book not found")
        existing_book.title = book_schema.title
        existing_book.author_id = book_schema.author_id
        existing_book.isbn = book_schema.isbn
        existing_book.price = book_schema.price
        existing_book.available_quantity = book_schema.available_quantity
        existing_book.category_id = book_schema.category_id
        existing_book.editorial_id = book_schema.editorial_id
        return self.book_repository.update(existing_book)

    def delete_book(self, book_id: int) -> None:
        existing_book = self.book_repository.get_by_id(book_id)
        if existing_book is None:
            raise HTTPException(status_code=404, detail= f"Book with ID {book_id} not found")

        self.book_repository.delete(book_id)