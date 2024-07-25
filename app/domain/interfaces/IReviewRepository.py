from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Review import Review

class IReviewRepository(ABC):
    @abstractmethod
    def add(self, review: Review) -> Review:
        pass

    @abstractmethod
    def get_by_id(self, review_id: int) -> Optional[Review]:
        pass

    @abstractmethod
    def get_all(self) -> List[Review]:
        pass

    @abstractmethod
    def update(self, review: Review) -> Review:
        pass

    @abstractmethod
    def delete(self, review_id: int) -> None:
        pass