from typing import Optional, List

from fastapi import HTTPException

from app.domain.interfaces.IPurchaseDetailRepository import IPurchaseDetailRepository
from app.domain.models.Book import Book
from app.domain.models.Purchase_Detail import Purchase_Detail
from app.adapters.api.schemas.PurchaseDetailSchema import PurchaseDetailSchema

class PurchaseDetailService:
    def __init__(self, purchase_detail_repository: IPurchaseDetailRepository):
        self.purchase_detail_repository = purchase_detail_repository

    def add_purchase_detail(self, purchase_detail_schema: PurchaseDetailSchema, book: Book) -> Purchase_Detail:
        purchase_detail = Purchase_Detail(
            purchase_id=purchase_detail_schema.purchase_id,
            customer_id=purchase_detail_schema.customer_id,
            book_id=purchase_detail_schema.book_id,
            quantity=purchase_detail_schema.quantity,
            unit_price=book.price
        )
        return self.purchase_detail_repository.add(purchase_detail)


    def get_purchase_detail_by_id(self, purchase_detail_id: int) -> Optional[Purchase_Detail]:
        return self.purchase_detail_repository.get_by_id(purchase_detail_id)

    def get_all_purchase_details(self) -> List[Purchase_Detail]:
        return self.purchase_detail_repository.get_all()

    def get_all_purchase_details_by_purchase_id(self, purchase_id: int) -> List[Purchase_Detail]:
        return self.purchase_detail_repository.get_all_by_purchase_id(purchase_id)

    def update_purchase_detail(self, purchase_detail_id: int, purchase_detail_schema: PurchaseDetailSchema) -> Purchase_Detail:
        existing_purchase_detail = self.purchase_detail_repository.get_by_id(purchase_detail_id)
        print(existing_purchase_detail.purchase_id)
        if existing_purchase_detail is None:
            raise ValueError("Purchase Detail not found")
        existing_purchase_detail.purchase_id = purchase_detail_schema.purchase_id
        existing_purchase_detail.customer_id = purchase_detail_schema.customer_id
        existing_purchase_detail.book_id = purchase_detail_schema.book_id
        existing_purchase_detail.quantity = purchase_detail_schema.quantity
        existing_purchase_detail.unit_price = purchase_detail_schema.unit_price
        return self.purchase_detail_repository.update(existing_purchase_detail)

    #def update_purchase_detail(self, purchase_detail_id: int, purchase_id: int) -> Purchase_Detail:
    #    existing_purchase_detail = self.purchase_detail_repository.get_by_id(purchase_detail_id)
    #    if existing_purchase_detail is None:
    #        raise ValueError("Purchase Detail not found")
    #    existing_purchase_detail.purchase_id = purchase_id
    #    return self.purchase_detail_repository.update(existing_purchase_detail)

    def delete_purchase_detail(self, purchase_detail_id: int) -> None:
        existing_purchase_detail = self.purchase_detail_repository.get_by_id(purchase_detail_id)
        if existing_purchase_detail is None:
            raise HTTPException(status_code=404, detail=f"Purchase Detail with ID {purchase_detail_id} not found")
        self.purchase_detail_repository.delete(purchase_detail_id)