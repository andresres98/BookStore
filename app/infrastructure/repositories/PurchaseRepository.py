from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.models.Purchase import Purchase
from app.domain.interfaces.IPurchaseRepository import IPurchaseRepository

class PurchaseRepository(IPurchaseRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, purchase: Purchase) -> Purchase:
        self.db_session.add(purchase)
        self.db_session.commit()
        self.db_session.refresh(purchase)
        return purchase

    def get_by_id(self, purchase_id: int) -> Optional[Purchase]:
        return self.db_session.query(Purchase).filter(Purchase.id == purchase_id).first()

    def get_all(self) -> List[Purchase]:
        return self.db_session.query(Purchase).all()

    def update(self, purchase: Purchase) -> Purchase:
        existing_purchase = self.db_session.merge(purchase)
        self.db_session.commit()
        return existing_purchase

    def delete(self, purchase_id: int) -> None:
        purchase_to_delete = self.db_session.query(Purchase).filter(Purchase.id == purchase_id).first()
        if purchase_to_delete:
            self.db_session.delete(purchase_to_delete)
            self.db_session.commit()