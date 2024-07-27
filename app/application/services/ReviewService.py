from typing import Optional, List
from app.domain.interfaces.IReviewRepository import IReviewRepository
from app.domain.models.Review import Review
from app.adapters.api.schemas.ReviewSchema import ReviewSchema

class ReviewService:
    def __init__(self, review_repository: IReviewRepository):
        self.review_repository = review_repository

    def add_review(self, review_schema: ReviewSchema) -> Review:
        review = Review(
            book_id=review_schema.book_id,
            customer_id=review_schema.customer_id,
            rating=review_schema.rating,
            comment=review_schema.comment
        )
        return self.review_repository.add(review)

    def get_review_by_id(self, review_id: int) -> Optional[Review]:
        return self.review_repository.get_by_id(review_id)

    def get_all_reviews(self) -> List[Review]:
        return self.review_repository.get_all()

    def update_review(self, review_id: int, review_schema: ReviewSchema) -> Review:
        existing_review = self.review_repository.get_by_id(review_id)
        if existing_review is None:
            raise ValueError("Review not found")
        existing_review.book_id = review_schema.book_id
        existing_review.customer_id = review_schema.customer_id
        existing_review.rating = review_schema.rating
        existing_review.comment = review_schema.comment
        return self.review_repository.update(existing_review)

    def delete_review(self, review_id: int) -> None:
        existing_review = self.review_repository.get_by_id(review_id)
        if existing_review is None:
            raise ValueError(f"Review with ID {review_id} not found")
        
        self.review_repository.delete(review_id)