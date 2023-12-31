from pydantic import UUID4, BaseModel

from src.dishes import schemas as dish_schemas


class SubmenuBase(BaseModel):
    title: str
    description: str


class Submenu(SubmenuBase):
    id: UUID4
    menu_id: UUID4
    dishes: list[dish_schemas.Dish] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SubmenuCreate(SubmenuBase):
    ...


class SubmenuCreateResponse(SubmenuBase):
    id: UUID4


class SubmenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
