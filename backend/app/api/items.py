from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import items as crud
from app.schemas.items import Item, ItemCreate
from app.database import get_db

router = APIRouter()

@router.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/categories/{category_id}/items/", response_model=List[Item])
def read_category_items(
    category_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    items = crud.get_items_by_category(db, category_id=category_id, skip=skip, limit=limit)
    return items

@router.post("/items/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = crud.update_item(db, item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}", response_model=bool)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return success

@router.patch("/items/{item_id}/quantity", response_model=Item)
def adjust_item_quantity(
    item_id: int, quantity_change: int, db: Session = Depends(get_db)
):
    updated_item = crud.update_item_quantity(db, item_id, quantity_change)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item 