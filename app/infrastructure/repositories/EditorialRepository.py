from typing import Optional, List

from sqlalchemy.orm import Session
from app.domain.models.Editorial import Editorial
from app.domain.interfaces.IEditorialRepository import IEditorialRepository

class EditorialRepository(IEditorialRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add(self, editorial: Editorial) -> Editorial:
        self.db_session.add(editorial)
        self.db_session.commit()
        self.db_session.refresh(editorial)
        return editorial

    def get_by_id(self, editorial_id: int) -> Optional[Editorial]:
        return self.db_session.query(Editorial).filter(Editorial.id == editorial_id).first()

    def get_all(self) -> List[Editorial]:
        return self.db_session.query(Editorial).all()

    def update(self, editorial: Editorial) -> Editorial:
        existing_editorial = self.db_session.merge(editorial)
        self.db_session.commit()
        return existing_editorial

    def delete(self, editorial_id: int) -> None:
        editorial_to_delete = self.db_session.query(Editorial).filter(Editorial.id == editorial_id).first()
        if editorial_to_delete:
            self.db_session.delete(editorial_to_delete)
            self.db_session.commit()