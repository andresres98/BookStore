from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.Customer import Customer

class ICustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def get_by_id(self, author_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def get_all(self) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete(self, customer_id: int) -> None:
        pass