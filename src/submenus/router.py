from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from src.submenus import schemas
from src.submenus.services import SubmenuService

router = APIRouter(prefix='/api/v1/menus')


@router.get(
    path='/{menu_id}/submenus',
    status_code=status.HTTP_200_OK,
    tags=['Submenus'],
)
async def list_menu_submenu(
    menu_id: UUID4,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenus_list = await submenu.list(menu_id)
    return jsonable_encoder(submenus_list)


@router.get(
    path='/{menu_id}/submenus/{submenu_id}',
    status_code=status.HTTP_200_OK,
    tags=['Submenus'],
)
async def get_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    response: Response,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenu_entity = await submenu.get(submenu_id)

    if not submenu_entity:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found'
        )
    return jsonable_encoder(submenu_entity)


@router.post(
    path='/{menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SubmenuCreateResponse,
    tags=['Submenus'],
)
async def post_menu_submenu(
    menu_id: UUID4,
    submenu_data: schemas.SubmenuCreate,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenu_entity = await submenu.create(submenu_data, menu_id)
    return jsonable_encoder(submenu_entity)


@router.patch(
    path='/{menu_id}/submenus/{submenu_id}',
    status_code=status.HTTP_200_OK,
    tags=['Submenus'],
)
async def patch_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    submenu_data: schemas.SubmenuUpdate,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenu_entity = await submenu.update(submenu_data, submenu_id)
    return jsonable_encoder(submenu_entity)


@router.delete(
    path='/{menu_id}/submenus/{submenu_id}',
    status_code=status.HTTP_200_OK,
    tags=['Submenus'],
)
async def delete_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    await submenu.delete(submenu_id)
