# app/application/services/CustomerService.py
from typing import Optional, List

from fastapi import HTTPException

from app.domain.interfaces.ICustomerRepository import ICustomerRepository
from app.domain.models.Customer import Customer
from app.adapters.api.schemas.CustomerSchema import CustomerSchema

class CustomerService:
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def add_customer(self, customer_schema: CustomerSchema) -> Customer:
        customer = Customer(
            name=customer_schema.name,
            email=customer_schema.email,
            phone=customer_schema.phone
        )
        return self.customer_repository.add(customer)

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.customer_repository.get_by_id(customer_id)

    def get_all_customers(self) -> List[Customer]:
        return self.customer_repository.get_all()

    def update_customer(self, customer_id: int, customer_schema: CustomerSchema) -> Customer:
        existing_customer = self.customer_repository.get_by_id(customer_id)
        if existing_customer is None:
            raise ValueError(f"Customer with ID {customer_id} not found")
        existing_customer.name = customer_schema.name
        existing_customer.email = customer_schema.email
        existing_customer.phone = customer_schema.phone
        return self.customer_repository.update(existing_customer)

    def delete_customer(self, customer_id: int) -> None:
        existing_customer = self.customer_repository.get_by_id(customer_id)
        if existing_customer is None:
            raise HTTPException(status_code=404, detail= f"Customer with ID {customer_id} not found")
        self.customer_repository.delete(customer_id)