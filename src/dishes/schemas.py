from typing import Optional
from decimal import Decimal

from pydantic import BaseModel

class DishBase(BaseModel):
    title: str
    description: str
    price: Decimal

class Dish(DishBase):
    id: str
    submenu_id: str

    class Config:
        from_attributes = True

class DishCreate(DishBase):
    ...

class DishResponse(DishBase):
    id: str
    price: str

class DishUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None