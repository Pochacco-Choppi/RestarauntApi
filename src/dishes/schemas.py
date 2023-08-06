from pydantic import UUID4, BaseModel, condecimal

DECIMAL_TYPE = condecimal(ge=0.009, decimal_places=2)


class DishBase(BaseModel):
    title: str
    description: str
    price: DECIMAL_TYPE  # type: ignore


class Dish(DishBase):
    id: UUID4
    submenu_id: UUID4

    class Config:
        from_attributes = True


class DishCreate(DishBase):
    ...


class DishCreateResponse(DishBase):
    id: UUID4


class DishUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: DECIMAL_TYPE | None = None  # type: ignore
