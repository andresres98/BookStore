# app/infrastructure/repositories/ReviewRepository.py
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.Review import Review
from app.domain.interfaces.IReviewRepository import IReviewRepository

class ReviewRepository(IReviewRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, review: Review) -> Review:
        self.db_session.add(review)
        self.db_session.commit()
        self.db_session.refresh(review)
        return review

    def get_by_id(self, review_id: int) -> Optional[Review]:
        return self.db_session.query(Review).filter(Review.id == review_id).first()

    def get_all(self) -> List[Review]:
        return self.db_session.query(Review).all()

    def update(self, review: Review) -> Review:
        existing_review = self.db_session.merge(review)
        self.db_session.commit()
        return existing_review

    def delete(self, review_id: int) -> None:
        review = self.db_session.query(Review).filter(Review.id == review_id).first()
        if review:
            self.db_session.delete(review)
            self.db_session.commit()