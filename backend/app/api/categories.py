from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import categories as crud
from app.schemas.categories import Category, CategoryCreate
from app.database import get_db

router = APIRouter()

@router.get("/categories/", response_model=List[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/categories/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category) 

@router.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.update_category(db, category_id, category)

@router.delete("/categories/{category_id}", response_model=bool)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db, category_id)