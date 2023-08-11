from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from src.menus import schemas
from src.menus.services import MenuService

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Menus'],
)


@router.get(
    path='/related/',
    status_code=status.HTTP_200_OK,
)
async def list_menu_with_related(menu: MenuService = Depends()) -> JSONResponse:
    menus_list = await menu.list_related()
    return jsonable_encoder(
        [schemas.Menu(
            id=m.id, 
            title=m.title, 
            description=m.description, 
            submenus=m.submenus,
            ) for m in menus_list]
    )

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
)
async def list_menu(menu: MenuService = Depends()) -> JSONResponse:
    menus_list = await menu.list_related()
    return jsonable_encoder(
        [schemas.MenuBase(
            # id=m.id, 
            title=m.title, 
            description=m.description, 
            # submenus=m.submenus,
            ) for m in menus_list]
    )


@router.get(
    path='/{menu_id}',
    status_code=status.HTTP_200_OK,
)
async def get_menu(
    menu_id: UUID4,
    response: Response,
    menu: MenuService = Depends(),
) -> JSONResponse:
    menu_entity = await menu.get(menu_id)

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
)
async def create_menu(
    menu_data: schemas.MenuCreate,
    menu: MenuService = Depends(),
) -> JSONResponse:
    menu_entity = await menu.create(menu_data)
    return jsonable_encoder(menu_entity)


@router.patch(
    path='/{menu_id}',
    status_code=status.HTTP_200_OK,
)
async def patch_menu(
    menu_id: UUID4,
    menu_data: schemas.MenuUpdate,
    menu: MenuService = Depends(),
) -> JSONResponse:
    menu_entity = await menu.update(menu_data, menu_id)
    return jsonable_encoder(menu_entity)


@router.delete(
    path='/{menu_id}',
    status_code=status.HTTP_200_OK,
)
async def delete_menu(menu_id: UUID4, menu: MenuService = Depends()) -> JSONResponse:
    await menu.delete(menu_id)
