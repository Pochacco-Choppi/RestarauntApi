from typing import Optional

from pydantic import BaseModel

from src.dishes.models import Dish

class SubmenuBase(BaseModel):
    title: str
    description: str

class Submenu(SubmenuBase):
    id: str
    menu_id: str
    dishes: list[Dish] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed=True

class SubmenuCreate(SubmenuBase):
    ...

class SubmenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None