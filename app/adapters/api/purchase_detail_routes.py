from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.application.services.BookService import BookService
from app.infrastructure.database import SessionLocal
from app.application.services.PurchaseDetailService import PurchaseDetailService
from app.application.services.PurchaseService import PurchaseService
from app.infrastructure.repositories.BookRepository import BookRepository
from app.infrastructure.repositories.PurchaseDetailRepository import PurchaseDetailRepository
from app.adapters.api.schemas.PurchaseDetailSchema import PurchaseDetailSchema
from typing import List

from app.infrastructure.repositories.PurchaseRepository import PurchaseRepository

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@router.post("/purchase_details/", response_model=PurchaseDetailSchema)
#def create_purchase_detail(purchase_detail: PurchaseDetailSchema = Body(...), db: Session = Depends(get_db)):
#    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
#    return purchase_detail_service.add_purchase_detail(purchase_detail)

@router.post("/purchase_details/", response_model=List[PurchaseDetailSchema])
def create_purchase_details(purchase_details: List[PurchaseDetailSchema] = Body(...), db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    created_purchase_details = []

    #Traer el purchase
    purchase_service = PurchaseService(PurchaseRepository(db))
    customer_id = purchase_details[0].customer_id
    purchase = purchase_service.add_purchase(customer_id)

    #Traer el libro
    book_service = BookService(BookRepository(db))
    book_id = purchase_details[0].book_id
    book = book_service.get_book_by_id(book_id)

    for purchase_detail in purchase_details:
        created_purchase_detail = purchase_detail_service.add_purchase_detail(purchase_detail, book)
        created_purchase_detail.purchase_id = purchase.id
        # Actualizar el purchase_id en el detalle pendiente
        updated_purchase_detail = purchase_detail_service.update_purchase_detail(created_purchase_detail.id, created_purchase_detail.purchase_id)
        created_purchase_details.append(updated_purchase_detail)
    return created_purchase_details

@router.get("/purchase_details/{purchase_detail_id}", response_model=PurchaseDetailSchema)
def read_purchase_detail(purchase_detail_id: int, db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    purchase_detail = purchase_detail_service.get_purchase_detail_by_id(purchase_detail_id)
    if purchase_detail is None:
        raise HTTPException(status_code=404, detail="Purchase Detail not found")
    return purchase_detail

@router.get("/purchase_details/", response_model=List[PurchaseDetailSchema])
def read_purchase_details(db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    purchase_details = purchase_detail_service.get_all_purchase_details()
    return purchase_details

@router.put("/purchase_details/{purchase_detail_id}", response_model=PurchaseDetailSchema)
def update_purchase_detail(purchase_detail_id: int, purchase_detail_schema: PurchaseDetailSchema = Body(...), db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    try:
        updated_purchase_detail = purchase_detail_service.update_purchase_detail(purchase_detail_id, purchase_detail_schema)
        return updated_purchase_detail
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/purchase_details/{purchase_detail_id}", status_code=200)
def delete_purchase_detail(purchase_detail_id: int, db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    purchase_detail_service.delete_purchase_detail(purchase_detail_id)
    return {"message": "Purchase Detail deleted successfully"}