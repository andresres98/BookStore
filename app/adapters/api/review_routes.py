from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.application.services.BookService import BookService
from app.application.services.CustomerService import CustomerService
from app.infrastructure.database import SessionLocal
from app.application.services.ReviewService import ReviewService
from app.infrastructure.repositories.BookRepository import BookRepository
from app.infrastructure.repositories.CustomerRepository import CustomerRepository
from app.infrastructure.repositories.ReviewRepository import ReviewRepository
from app.adapters.api.schemas.ReviewSchema import ReviewSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reviews/", response_model=ReviewSchema)
def create_review(review: ReviewSchema = Body(...), db: Session = Depends(get_db)):
    review_service = ReviewService(ReviewRepository(db))
    book_service = BookService(BookRepository(db))
    customer_service = CustomerService(CustomerRepository(db))

    book = book_service.get_book_by_id(review.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {review.book_id} not found")

    customer = customer_service.get_customer_by_id(review.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer with ID {review.customer_id} not found")

    return review_service.add_review(review)

@router.get("/reviews/{review_id}", response_model=ReviewSchema)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review_service = ReviewService(ReviewRepository(db))
    review = review_service.get_review_by_id(review_id)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.get("/reviews/", response_model=List[ReviewSchema])
def read_reviews(db: Session = Depends(get_db)):
    review_service = ReviewService(ReviewRepository(db))
    reviews = review_service.get_all_reviews()
    return reviews

@router.put("/reviews/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, review_schema: ReviewSchema = Body(...), db: Session = Depends(get_db)):
    review_service = ReviewService(ReviewRepository(db))
    book_service = BookService(BookRepository(db))
    customer_service = CustomerService(CustomerRepository(db))

    book = book_service.get_book_by_id(review_schema.book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {review_schema.book_id} not found")

    customer = customer_service.get_customer_by_id(review_schema.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail=f"Customer with ID {review_schema.customer_id} not found")

    updated_review = review_service.update_review(review_id, review_schema)
    return updated_review

@router.delete("/reviews/{review_id}", status_code=200)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_service = ReviewService(ReviewRepository(db))
    try:
        review_service.delete_review(review_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Review deleted successfully"}