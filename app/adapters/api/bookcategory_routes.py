from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.application.services.BookCategoryService import BookCategoryService
from app.infrastructure.repositories.BookCategoryRepository import BookCategoryRepository
from app.adapters.api.schemas.BookCategorySchema import BookCategorySchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/book-categories/", response_model=BookCategorySchema)
def create_book_category(book_category: BookCategorySchema = Body(...), db: Session = Depends(get_db)):
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    return book_category_service.add_book_category(book_category)

@router.get("/book-categories/{book_category_id}", response_model=BookCategorySchema)
def read_book_category(book_category_id: int, db: Session = Depends(get_db)):
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    book_category = book_category_service.get_book_category_by_id(book_category_id)
    if book_category is None:
        raise HTTPException(status_code=404, detail="BookCategory not found")
    return book_category

@router.get("/book-categories/", response_model=List[BookCategorySchema])
def read_book_categories(db: Session = Depends(get_db)):
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    book_categories = book_category_service.get_all_book_categories()
    return book_categories

@router.put("/book-categories/{book_category_id}", response_model=BookCategorySchema)
def update_book_category(book_category_id: int, book_category_schema: BookCategorySchema = Body(...), db: Session = Depends(get_db)):
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    existing_book_category = book_category_service.get_book_category_by_id(book_category_id)
    if existing_book_category is None:
        raise HTTPException(status_code=404, detail="BookCategory not found")

    existing_book_category.name = book_category_schema.name

    updated_book_category = book_category_service.update_book_category(existing_book_category)
    return updated_book_category

#@router.delete("/book-categories/{book_category_id}", status_code=200)
#def delete_book_category(book_category_id: int, db: Session = Depends(get_db)):
#    from fastapi import HTTPException

@router.delete("/book-categories/{book_category_id}", status_code=200)
def delete_book_category(book_category_id: int, db: Session = Depends(get_db)):
    book_category_service = BookCategoryService(BookCategoryRepository(db))
    try:
        book_category_service.delete_book_category(book_category_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return {"message": "BookCategory deleted successfully"}