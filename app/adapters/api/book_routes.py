from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.application.services.BookService import BookService
from app.infrastructure.repositories.BookRepository import BookRepository
from app.adapters.api.schemas.BookSchema import BookSchema
from typing import List

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
    try:
        updated_book = book_service.update_book(book_id, book_schema)
        return updated_book
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/books/{book_id}", status_code=200)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_service = BookService(BookRepository(db))
    book_service.delete_book(book_id)
    return {"message": "Book deleted successfully"}