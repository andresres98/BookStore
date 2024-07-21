
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Book_Category import BookCategory

class IBookCategoryRepository(ABC):
    @abstractmethod
    def add(self, book_category: BookCategory) -> BookCategory:
        pass

    @abstractmethod
    def get_by_id(self, book_category_id: int) -> Optional[BookCategory]:
        pass

    @abstractmethod
    def get_all(self) -> List[BookCategory]:
        pass

    @abstractmethod
    def update(self, book_category: BookCategory) -> BookCategory:
        pass

    @abstractmethod
    def delete(self, book_category_id: int) -> None:
        pass