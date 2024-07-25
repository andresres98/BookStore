from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.Customer import Customer
from app.domain.interfaces.ICustomerRepository import ICustomerRepository

class CustomerRepository(ICustomerRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, customer: Customer) -> Customer:
        self.db_session.add(customer)
        self.db_session.commit()
        self.db_session.refresh(customer)
        return customer

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.db_session.query(Customer).filter(Customer.id == customer_id).first()

    def get_all(self) -> List[Customer]:
        return self.db_session.query(Customer).all()

    def update(self, customer: Customer) -> Customer:
        existing_customer = self.db_session.query(Customer).filter(Customer.id == customer.id).first()
        if existing_customer:
            existing_customer.name = customer.name
            existing_customer.email = customer.email
            existing_customer.phone = customer.phone
            self.db_session.commit()
            self.db_session.refresh(existing_customer)
        return existing_customer

    def delete(self, customer_id: int) -> None:
        customer = self.db_session.query(Customer).filter(Customer.id == customer_id).first()
        if customer:
            self.db_session.delete(customer)
            self.db_session.commit()