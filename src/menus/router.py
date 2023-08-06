from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from src.menus import schemas
from src.menus.services import MenuService

router = APIRouter(prefix='/api/v1/menus')


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Menus'],
)
async def list_menu(menu: MenuService = Depends()) -> JSONResponse:
    menus_list = await menu.list()
    return jsonable_encoder(
        [schemas.MenuBase(title=m.title, description=m.description) for m in menus_list]
    )


@router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Menus'],
)
async def get_menu(
    id: UUID4,
    response: Response,
    menu: MenuService = Depends(),
) -> JSONResponse:
    menu_entity = await menu.get(id)

    if not menu_entity:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='menu not found'
        )
    return jsonable_encoder(menu_entity)


@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MenuCreateResponse,
    tags=['Menus'],
)
async def create_menu(
    menu_data: schemas.MenuCreate,
    menu: MenuService = Depends(),
) -> JSONResponse:
    menu_entity = await menu.create(menu_data)
    return jsonable_encoder(menu_entity)


@router.patch(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Menus'],
)
async def patch_menu(
    id: UUID4,
    menu_data: schemas.MenuUpdate,
    menu: MenuService = Depends(),
) -> JSONResponse:
    menu_entity = await menu.update(menu_data, id)
    return jsonable_encoder(menu_entity)


@router.delete(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    tags=['Menus'],
)
async def delete_menu(id: UUID4, menu: MenuService = Depends()) -> JSONResponse:
    await menu.delete(id)
