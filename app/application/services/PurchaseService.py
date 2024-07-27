import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy.types import DateTime
from app.domain.interfaces.IPurchaseRepository import IPurchaseRepository
from app.application.services.PurchaseDetailService import PurchaseDetailService
from app.domain.models.Purchase import Purchase
from app.adapters.api.schemas.PurchaseSchema import PurchaseSchema

class PurchaseService:
    def __init__(self, purchase_repository: IPurchaseRepository):
        self.purchase_repository = purchase_repository

    def add_purchase(self, purchase_schema: PurchaseSchema) -> Purchase:
        purchase = Purchase(
            customer_id=purchase_schema.customer_id,
            date=DateTime(default=datetime.datetime.now),
            total_amount=purchase_schema.total_amount
        )
        return self.purchase_repository.add(purchase)

    def add_purchase(self, customer_id: int) -> Purchase:
        purchase = Purchase(
            customer_id=customer_id,
            date=datetime.date.today(),
            total_amount=0
        )
        return self.purchase_repository.add(purchase)

    def get_purchase_by_id(self, purchase_id: int) -> Optional[Purchase]:
        return self.purchase_repository.get_by_id(purchase_id)

    def get_all_purchases(self) -> List[Purchase]:
        return self.purchase_repository.get_all()

    def update_purchase(self, purchase_id: int, purchase_schema: PurchaseSchema) -> Purchase:
        existing_purchase = self.purchase_repository.get_by_id(purchase_id)
        if existing_purchase is None:
            raise ValueError("Purchase not found")
        existing_purchase.customer_id = purchase_schema.customer_id
        existing_purchase.date = purchase_schema.date
        existing_purchase.total_amount = purchase_schema.total_amount
        return self.purchase_repository.update(existing_purchase)

    def update_purchase_total_amount(self, purchase_id: int, total_amount: float) -> Purchase:
        existing_purchase = self.purchase_repository.get_by_id(purchase_id)
        if existing_purchase is None:
            raise ValueError("Purchase not found")
        existing_purchase.total_amount = total_amount
        return self.purchase_repository.update(existing_purchase)

    def delete_purchase(self, purchase_id: int) -> None:
        existing_purchase = self.purchase_repository.get_by_id(purchase_id)
        if existing_purchase is None:
            raise HTTPException(status_code=404, detail=f"Purchase with ID {purchase_id} not found")
        self.purchase_repository.delete(purchase_id)