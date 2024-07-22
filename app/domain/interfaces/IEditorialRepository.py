from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Editorial import Editorial

class IEditorialRepository(ABC):
    @abstractmethod
    def add(self, editorial: Editorial) -> Editorial:
        pass

    @abstractmethod
    def get_by_id(self, editorial_id: int) -> Optional[Editorial]:
        pass

    @abstractmethod
    def get_all(self) -> List[Editorial]:
        pass

    @abstractmethod
    def update(self, editorial: Editorial) -> Editorial:
        pass

    @abstractmethod
    def delete(self, editorial_id: int) -> None:
        pass