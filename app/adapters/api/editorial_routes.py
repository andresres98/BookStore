from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.application.services.EditorialService import EditorialService
from app.infrastructure.repositories.EditorialRepository import EditorialRepository
from app.adapters.api.schemas.EditorialSchema import EditorialSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/editorials/", response_model=EditorialSchema)
def create_editorial(editorial: EditorialSchema = Body(...), db: Session = Depends(get_db)):
    editorial_service = EditorialService(EditorialRepository(db))
    return editorial_service.add_editorial(editorial)

@router.get("/editorials/{editorial_id}", response_model=EditorialSchema)
def read_editorial(editorial_id: int, db: Session = Depends(get_db)):
    editorial_service = EditorialService(EditorialRepository(db))
    editorial = editorial_service.get_editorial_by_id(editorial_id)
    if editorial is None:
        raise HTTPException(status_code=404, detail="Editorial not found")
    return editorial

@router.get("/editorials/", response_model=List[EditorialSchema])
def read_editorials(db: Session = Depends(get_db)):
    editorial_service = EditorialService(EditorialRepository(db))
    editorials = editorial_service.get_all_editorials()
    return editorials

@router.put("/editorials/{editorial_id}", response_model=EditorialSchema)
def update_editorial(editorial_id: int, editorial_schema: EditorialSchema = Body(...), db: Session = Depends(get_db)):
    editorial_service = EditorialService(EditorialRepository(db))
    try:
        updated_editorial = editorial_service.update_editorial(editorial_id, editorial_schema)
        return updated_editorial
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/editorials/{editorial_id}", status_code=200)
def delete_editorial(editorial_id: int, db: Session = Depends(get_db)):
    editorial_service = EditorialService(EditorialRepository(db))
    try:
        editorial_service.delete_editorial(editorial_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return {"message": "Editorial deleted successfully"}