from sqlalchemy.orm import Session
from app.models import Item
from app.schemas.items import ItemCreate

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(Item)\
        .filter(Item.category_id == category_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemCreate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        for key, value in item.model_dump().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

def update_item_quantity(db: Session, item_id: int, quantity_change: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.quantity += quantity_change
        db.commit()
        db.refresh(db_item)
    return db_item 