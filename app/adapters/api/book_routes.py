from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.application.services.AuthorService import AuthorService
from app.application.services.BookCategoryService import BookCategoryService
from app.application.services.EditorialService import EditorialService
from app.infrastructure.database import SessionLocal
from app.application.services.BookService import BookService
from app.infrastructure.repositories.AuthorRepository import AuthorRepository
from app.infrastructure.repositories.BookCategoryRepository import BookCategoryRepository
from app.infrastructure.repositories.BookRepository import BookRepository
from app.adapters.api.schemas.BookSchema import BookSchema
from typing import List

from app.infrastructure.repositories.EditorialRepository import EditorialRepository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/books/", response_model=BookSchema)
def create_book(book: BookSchema = Body(...), db: Session = Depends(get_db)):
    book_service = BookService(BookRepository(db))
    author_service = AuthorService(AuthorRepository(db))
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    editorial_service = EditorialService(EditorialRepository(db))


    author = author_service.get_author_by_id(book.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail=f"Author with ID {book.author_id} not found")

    editorial = editorial_service.get_editorial_by_id(book.editorial_id)
    if editorial is None:
        raise HTTPException(status_code=404, detail=f"Editorial with ID {book.editorial_id} not found")

    book_category = book_category_service.get_book_category_by_id(book.category_id)
    if book_category is None:
        raise HTTPException(status_code=404, detail=f"Category with ID {book.category_id} not found")

    return book_service.add_book(book)

@router.get("/books/{book_id}", response_model=BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book_service = BookService(BookRepository(db))
    book = book_service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/books/", response_model=List[BookSchema])
def read_books(db: Session = Depends(get_db)):
    book_service = BookService(BookRepository(db))
    books = book_service.get_all_books()
    return books

@router.put("/books/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book_schema: BookSchema = Body(...), db: Session = Depends(get_db)):
    book_service = BookService(BookRepository(db))
    author_service = AuthorService(AuthorRepository(db))
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    editorial_service = EditorialService(EditorialRepository(db))

    book = book_service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    author = author_service.get_author_by_id(book_schema.author_id)
    if author is None:
        raise HTTPException(status_code=404, detail=f"Author with ID {book_schema.author_id} not found")

    editorial = editorial_service.get_editorial_by_id(book_schema.editorial_id)
    if editorial is None:
        raise HTTPException(status_code=404, detail=f"Editorial with ID {book_schema.editorial_id} not found")

    book_category = book_category_service.get_book_category_by_id(book_schema.category_id)
    if book_category is None:
        raise HTTPException(status_code=404, detail=f"Category with ID {book_schema.category_id} not found")

    updated_book = book_service.update_book(book_id, book_schema)
    return updated_book


@router.delete("/books/{book_id}", status_code=200)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_service = BookService(BookRepository(db))
    book_service.delete_book(book_id)
    return {"message": "Book deleted successfully"}