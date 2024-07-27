# app/adapters/api/customer_routes.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.application.services.CustomerService import CustomerService
from app.infrastructure.repositories.CustomerRepository import CustomerRepository
from app.adapters.api.schemas.CustomerSchema import CustomerSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/customers/", response_model=CustomerSchema)
def create_customer(customer: CustomerSchema = Body(...), db: Session = Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    return customer_service.add_customer(customer)

@router.get("/customers/{customer_id}", response_model=CustomerSchema)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    customer = customer_service.get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/customers/", response_model=List[CustomerSchema])
def read_customers(db: Session = Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    customers = customer_service.get_all_customers()
    return customers

@router.put("/customers/{customer_id}", response_model=CustomerSchema)
def update_customer(customer_id: int, customer_schema: CustomerSchema = Body(...), db: Session = Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    try:
        updated_customer = customer_service.update_customer(customer_id, customer_schema)
        return updated_customer
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/customers/{customer_id}", status_code=200)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer_service = CustomerService(CustomerRepository(db))
    try:
        customer_service.delete_customer(customer_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "Customer deleted successfully"}