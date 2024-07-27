from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.application.services.PurchaseDetailService import PurchaseDetailService
from app.infrastructure.database import SessionLocal
from app.application.services.PurchaseService import PurchaseService
from app.infrastructure.repositories.PurchaseDetailRepository import PurchaseDetailRepository
from app.infrastructure.repositories.PurchaseRepository import PurchaseRepository
from app.adapters.api.schemas.PurchaseSchema import PurchaseSchema
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@router.post("/purchases/", response_model=PurchaseSchema)
#def create_purchase(purchase: PurchaseSchema = Body(...), db: Session = Depends(get_db)):
#    purchase_service = PurchaseService(PurchaseRepository(db))
#    return purchase_service.add_purchase(purchase)

@router.get("/purchases/{purchase_id}", response_model=PurchaseSchema)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase_service = PurchaseService(PurchaseRepository(db))
    purchase = purchase_service.get_purchase_by_id(purchase_id)
    if purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

@router.get("/purchases/", response_model=List[PurchaseSchema])
def read_purchases(db: Session = Depends(get_db)):
    purchase_service = PurchaseService(PurchaseRepository(db))
    purchases = purchase_service.get_all_purchases()
    return purchases

#@router.put("/purchases/{purchase_id}", response_model=PurchaseSchema)
#def update_purchase(purchase_id: int, purchase_schema: PurchaseSchema = Body(...), db: Session = Depends(get_db)):
#    purchase_service = PurchaseService(PurchaseRepository(db))
#    try:
#        updated_purchase = purchase_service.update_purchase(purchase_id, purchase_schema)
#        return updated_purchase
#    except ValueError as e:
#        raise HTTPException(status_code=404, detail=str(e))

#@router.delete("/purchases/{purchase_id}", status_code=200)
#def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
#    purchase_service = PurchaseService(PurchaseRepository(db))
#    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
#    try:
#        details = purchase_detail_service.get_purchase_detail_by_id(purchase_id)
#        print(type(details))
#        for detail in details:
#            purchase_detail_service.delete_purchase_detail(detail.id)
#
#        purchase_service.delete_purchase(purchase_id)
#    except HTTPException as e:
#        raise HTTPException(status_code=404, detail=str(e))
#
#    return {"message": "Purchase deleted successfully"}