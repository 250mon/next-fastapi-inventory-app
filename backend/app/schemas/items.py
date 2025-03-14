from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None
    quantity: int
    category_id: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True 