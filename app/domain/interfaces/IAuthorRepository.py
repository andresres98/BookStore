
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Author import Author

class IAuthorRepository(ABC):
    @abstractmethod
    def add(self, author: Author) -> Author:
        pass

    @abstractmethod
    def get_by_id(self, author_id: int) -> Optional[Author]:
        pass

    @abstractmethod
    def get_all(self) -> List[Author]:
        pass

    @abstractmethod
    def update(self, author: Author) -> Author:
        pass

    @abstractmethod
    def delete(self, author_id: int) -> None:
        pass