from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models.Purchase_Detail import Purchase_Detail
from app.domain.interfaces.IPurchaseDetailRepository import IPurchaseDetailRepository

class PurchaseDetailRepository(IPurchaseDetailRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, purchase_detail: Purchase_Detail) -> Purchase_Detail:
        self.db_session.add(purchase_detail)
        self.db_session.commit()
        self.db_session.refresh(purchase_detail)
        return purchase_detail

    def get_by_id(self, purchase_detail_id: int) -> Optional[Purchase_Detail]:
        return self.db_session.query(Purchase_Detail).filter(Purchase_Detail.id == purchase_detail_id).first()

    def get_all(self) -> List[Purchase_Detail]:
        return self.db_session.query(Purchase_Detail).all()

    def get_all_by_purchase_id(self, purchase_id: int) -> List[Purchase_Detail]:
        return self.db_session.query(Purchase_Detail).filter(Purchase_Detail.purchase_id == purchase_id).all()

    def update(self, purchase_detail: Purchase_Detail) -> Purchase_Detail:
        existing_purchase_detail = self.db_session.merge(purchase_detail)
        self.db_session.commit()
        return existing_purchase_detail

    def delete(self, purchase_detail_id: int) -> None:
        purchase_detail_to_delete = self.db_session.query(Purchase_Detail).filter(Purchase_Detail.id == purchase_detail_id).first()
        if purchase_detail_to_delete:
            self.db_session.delete(purchase_detail_to_delete)
            self.db_session.commit()