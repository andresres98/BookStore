from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.application.services.BookService import BookService
from app.application.services.CustomerService import CustomerService
from app.infrastructure.database import SessionLocal
from app.application.services.PurchaseDetailService import PurchaseDetailService
from app.application.services.PurchaseService import PurchaseService
from app.infrastructure.repositories.BookRepository import BookRepository
from app.infrastructure.repositories.CustomerRepository import CustomerRepository
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
def create_purchase_details(items: List[dict] = Body(...), db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    customer_service = CustomerService(CustomerRepository(db))
    book_service = BookService(BookRepository(db))
    created_purchase_details = []
    purchase_details = []

    for item in items:
        purchase_detail_schema = PurchaseDetailSchema
        if customer_service.get_customer_by_id(item['customer_id']) is None:
            raise HTTPException(status_code=404, detail=f"Customer with ID {item['customer_id']} not found")
        purchase_detail_schema.customer_id = item['customer_id']
        if book_service.get_book_by_id(item['book_id']) is None:
            raise HTTPException(status_code=404, detail=f"Book with ID {item['book_id']} not found")
        purchase_detail_schema.book_id = item['book_id']
        purchase_detail_schema.quantity = item['quantity']
        purchase_details.append(purchase_detail_schema)


    #Traer el purchase
    purchase_service = PurchaseService(PurchaseRepository(db))
    customer_id = purchase_details[0].customer_id
    purchase = purchase_service.add_purchase(customer_id)

    #Traer el libro
    book_service = BookService(BookRepository(db))


    for purchase_detail in purchase_details:
        book_id = purchase_detail.book_id
        book = book_service.get_book_by_id(book_id)
        purchase_detail.purchase_id = purchase.id
        created_purchase_detail = purchase_detail_service.add_purchase_detail(purchase_detail, book)
        created_purchase_details.append(created_purchase_detail)

    total = 0
    for detail in created_purchase_details:
        total += (detail.quantity * detail.unit_price)

    purchase_service.update_purchase_total_amount(purchase.id, total)
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
    purchase_detail = purchase_detail_service.get_purchase_detail_by_id(purchase_detail_id)

    if purchase_detail is None:
        raise HTTPException(status_code=404, detail="Purchase Detail not found")

    updated_purchase_detail = purchase_detail_service.update_purchase_detail(purchase_detail_id, purchase_detail_schema)
    return updated_purchase_detail

@router.delete("/purchase_details/{purchase_detail_id}", status_code=200)
def delete_purchase_detail(purchase_detail_id: int, db: Session = Depends(get_db)):
    purchase_detail_service = PurchaseDetailService(PurchaseDetailRepository(db))
    try:
        purchase_detail_service.delete_purchase_detail(purchase_detail_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Purchase Detail deleted successfully"}