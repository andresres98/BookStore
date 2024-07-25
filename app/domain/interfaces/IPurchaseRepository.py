from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Purchase import Purchase

class IPurchaseRepository(ABC):
    @abstractmethod
    def add(self, purchase: Purchase) -> Purchase:
        pass

    @abstractmethod
    def get_by_id(self, purchase_id: int) -> Optional[Purchase]:
        pass

    @abstractmethod
    def get_all(self) -> List[Purchase]:
        pass

    @abstractmethod
    def update(self, purchase: Purchase) -> Purchase:
        pass

    @abstractmethod
    def delete(self, purchase_id: int) -> None:
        pass