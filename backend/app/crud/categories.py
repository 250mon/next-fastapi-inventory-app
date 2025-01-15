from sqlalchemy.orm import Session
from app.models import Category
from app.schemas.categories import CategoryCreate

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category 

def update_category(db: Session, category_id: int, category: CategoryCreate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        for key, value in category.model_dump().items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False
