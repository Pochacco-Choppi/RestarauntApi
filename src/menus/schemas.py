from typing import Optional

from pydantic import BaseModel, UUID4

from src.submenus.models import Submenu


class MenuBase(BaseModel):
    title: str
    description: str

class Menu(MenuBase):
    id: UUID4
    submenus: list[Submenu] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class MenuCreate(MenuBase):
    ...

class MenuCreateResponse(MenuBase):
    id: UUID4

class MenuUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
