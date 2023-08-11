from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from src.dishes import schemas
from src.dishes.constants import DICIMAL_FLOAT_TO_STR
from src.dishes.services import DishService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['Dishes'],
)


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
)
async def list_dish(
    submenu_id: UUID4,
    dish: DishService = Depends(),
) -> JSONResponse:
    dishes_list = await dish.list(submenu_id)
    return jsonable_encoder(dishes_list)


@router.get(
    path='/{dish_id}',
    status_code=status.HTTP_200_OK,
)
async def get_dish(
    dish_id: UUID4,
    menu_id: UUID4,
    submenu_id: UUID4,
    response: Response,
    dish: DishService = Depends(),
) -> JSONResponse:
    dish_entity = await dish.get(dish_id, menu_id, submenu_id)

    if not dish_entity:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='dish not found'
        )

    return jsonable_encoder(dish_entity, custom_encoder=DICIMAL_FLOAT_TO_STR)


@router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DishCreateResponse,
)
async def create_dish(
    submenu_id: UUID4,
    menu_id: UUID4,
    dish_data: schemas.DishCreate,
    dish: DishService = Depends(),
) -> JSONResponse:
    dish_entity = await dish.create(dish_data, submenu_id, menu_id)
    return jsonable_encoder(dish_entity, custom_encoder=DICIMAL_FLOAT_TO_STR)


@router.patch(
    path='/{dish_id}',
    status_code=status.HTTP_200_OK,
)
async def patch_dish(
    dish_id: UUID4,
    submenu_id: UUID4,
    menu_id: UUID4,
    dish_data: schemas.DishUpdate,
    dish: DishService = Depends(),
) -> JSONResponse:
    dish_entity = await dish.update(dish_data, dish_id, menu_id, submenu_id)
    return jsonable_encoder(dish_entity, custom_encoder=DICIMAL_FLOAT_TO_STR)


@router.delete(
    path='/{dish_id}',
    status_code=status.HTTP_200_OK,
)
async def delete_dish(
    dish_id: UUID4,
    menu_id: UUID4,
    submenu_id: UUID4,
    dish: DishService = Depends(),
) -> JSONResponse:
    await dish.delete(dish_id, menu_id, submenu_id)
