from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.application.services.PurchaseService import PurchaseService
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

@router.post("/purchases/", response_model=PurchaseSchema)
def create_purchase(purchase: PurchaseSchema = Body(...), db: Session = Depends(get_db)):
    purchase_service = PurchaseService(PurchaseRepository(db))
    return purchase_service.add_purchase(purchase)

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
    print(purchases)
    return purchases

@router.put("/purchases/{purchase_id}", response_model=PurchaseSchema)
def update_purchase(purchase_id: int, purchase_schema: PurchaseSchema = Body(...), db: Session = Depends(get_db)):
    purchase_service = PurchaseService(PurchaseRepository(db))
    try:
        updated_purchase = purchase_service.update_purchase(purchase_id, purchase_schema)
        return updated_purchase
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/purchases/{purchase_id}", status_code=200)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase_service = PurchaseService(PurchaseRepository(db))
    purchase_service.delete_purchase(purchase_id)
    return {"message": "Purchase deleted successfully"}