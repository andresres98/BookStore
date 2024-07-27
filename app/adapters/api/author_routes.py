from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.application.services.AuthorService import AuthorService
from app.infrastructure.repositories.AuthorRepository import AuthorRepository

from app.adapters.api.schemas.AuthorSchema import AuthorSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/authors/", response_model=AuthorSchema)
def create_author(author: AuthorSchema = Body(...), db: Session = Depends(get_db)):
    author_service = AuthorService(AuthorRepository(db))
    return author_service.add_author(author)

@router.get("/authors/{author_id}", response_model=AuthorSchema)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author_service = AuthorService(AuthorRepository(db))
    author = author_service.get_author_by_id(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.get("/authors/", response_model=List[AuthorSchema])
def read_authors(db: Session = Depends(get_db)):
    author_service = AuthorService(AuthorRepository(db))
    authors = author_service.get_all_authors()
    return authors

@router.put("/authors/{author_id}", response_model=AuthorSchema)
def update_author(author_id: int, author_schema: AuthorSchema = Body(...), db: Session = Depends(get_db)):
    author_service = AuthorService(AuthorRepository(db))
    try:
        updated_author = author_service.update_author(author_id, author_schema)
        return updated_author
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/authors/{author_id}", status_code=200)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author_service = AuthorService(AuthorRepository(db))
    try:
        author_service.delete_author(author_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return {"message": "Author deleted successfully"}