from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Relationships
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Relationships
    category = relationship("Category", back_populates="items")
    transactions = relationship("Transaction", back_populates="item")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity_change = Column(Integer)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    transaction_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    item = relationship("Item", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
