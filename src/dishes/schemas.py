from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, UUID4, Field, condecimal

DECIMAL_TYPE = condecimal(ge=0.009, decimal_places=2)

class DishBase(BaseModel):
    title: str
    description: str
    price: DECIMAL_TYPE

class Dish(DishBase):
    id: UUID4
    submenu_id: UUID4

    class Config:
        from_attributes = True

class DishCreate(DishBase):
    ...

class DishResponse(DishBase):
    id: UUID4
    price: DECIMAL_TYPE

class DishUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[DECIMAL_TYPE] = None