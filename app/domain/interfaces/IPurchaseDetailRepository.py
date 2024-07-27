from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Purchase_Detail import Purchase_Detail

class IPurchaseDetailRepository(ABC):
    @abstractmethod
    def add(self, purchase_detail: Purchase_Detail) -> Purchase_Detail:
        pass

    @abstractmethod
    def get_by_id(self, purchase_detail_id: int) -> Optional[Purchase_Detail]:
        pass

    @abstractmethod
    def get_all(self) -> List[Purchase_Detail]:
        pass

    @abstractmethod
    def get_all_by_purchase_id(self, purchase_id: int) -> List[Purchase_Detail]:
        pass

    @abstractmethod
    def update(self, purchase_detail: Purchase_Detail) -> Purchase_Detail:
        pass

    @abstractmethod
    def delete(self, purchase_detail_id: int) -> None:
        pass