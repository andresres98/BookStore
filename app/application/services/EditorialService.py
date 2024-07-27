from typing import Optional, List

from fastapi import HTTPException

from app.domain.interfaces.IEditorialRepository import IEditorialRepository
from app.domain.models.Editorial import Editorial
from app.adapters.api.schemas.EditorialSchema import EditorialSchema

class EditorialService:
    def __init__(self, editorial_repository: IEditorialRepository):
        self.editorial_repository = editorial_repository

    def add_editorial(self, editorial_schema: EditorialSchema) -> Editorial:
        editorial = Editorial(
            name=editorial_schema.name,
            address=editorial_schema.address,
            country=editorial_schema.country
        )
        return self.editorial_repository.add(editorial)

    def get_editorial_by_id(self, editorial_id: int) -> Optional[Editorial]:
        return self.editorial_repository.get_by_id(editorial_id)

    def get_all_editorials(self) -> List[Editorial]:
        return self.editorial_repository.get_all()

    def update_editorial(self, editorial_id: int, editorial_schema: EditorialSchema) -> Editorial:
        existing_editorial = self.editorial_repository.get_by_id(editorial_id)
        if existing_editorial is None:
            raise ValueError("Editorial not found")
        existing_editorial.name = editorial_schema.name
        existing_editorial.address = editorial_schema.address
        existing_editorial.country = editorial_schema.country
        return self.editorial_repository.update(existing_editorial)

    def delete_editorial(self, editorial_id: int) -> None:
        existing_editorial = self.editorial_repository.get_by_id(editorial_id)
        if existing_editorial is None:
            raise HTTPException(status_code=404,detail=f"Editorial with ID {editorial_id} not found")
        self.editorial_repository.delete(editorial_id)