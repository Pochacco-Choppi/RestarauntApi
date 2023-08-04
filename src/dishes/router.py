from fastapi import Depends, APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.dishes.constants import DICIMAL_FLOAT_TO_STR
from src.dishes import schemas
from src.dishes.crud import DishRepository
from src.dependencies import get_session

router = APIRouter(prefix="/api/v1/menus")


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    status_code=status.HTTP_200_OK,
    tags=["Dishes"],
)
async def list_submenu_dishes(
    submenu_id: UUID4,
    dish: DishRepository = Depends(),
) -> JSONResponse:
    dishes = await dish.list_submenu_dishes(submenu_id)
    return jsonable_encoder(dishes)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
    tags=["Dishes"],
)
async def get_dish(
    dish_id: UUID4,
    response: Response,
    dish: DishRepository = Depends(),
) -> JSONResponse:
    dish = await dish.get(dish_id)

    if not dish:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )

    return jsonable_encoder(dish, custom_encoder=DICIMAL_FLOAT_TO_STR)


@router.post(
    path="/{menu_id}/submenus/{submenu_id}/dishes",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DishCreateResponse,
    tags=["Dishes"],
)
async def post_submenu_dish(
    submenu_id: UUID4,
    dish_data: schemas.DishCreate,
    dish: DishRepository = Depends(),
) -> JSONResponse:
    dish = await dish.create_submenu_dish(dish_data, submenu_id)
    return jsonable_encoder(dish, custom_encoder=DICIMAL_FLOAT_TO_STR)


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
    tags=["Dishes"],
)
async def patch_dish(
    dish_id: UUID4,
    dish_data: schemas.DishUpdate,
    dish: DishRepository = Depends(),
) -> JSONResponse:
    dish = await dish.update(dish_data, dish_id)
    return jsonable_encoder(dish, custom_encoder=DICIMAL_FLOAT_TO_STR)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    status_code=status.HTTP_200_OK,
    tags=["Dishes"],
)
async def delete_dish(
    dish_id: UUID4,
    dish: DishRepository = Depends(),
) -> JSONResponse:
    await dish.delete(dish_id)
