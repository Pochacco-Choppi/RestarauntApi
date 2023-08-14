from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4

from src.submenus import schemas
from src.submenus.services import SubmenuService

router = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['Submenus'],
)


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
)
async def list_submenu(
    menu_id: UUID4,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenus_list = await submenu.list(menu_id)
    return jsonable_encoder(submenus_list)


@router.get(
    path='/{submenu_id}',
    status_code=status.HTTP_200_OK,
)
async def get_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    response: Response,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenu_entity = await submenu.get(submenu_id, menu_id)

    if not submenu_entity:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found'
        )
    return jsonable_encoder(submenu_entity)


@router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SubmenuCreateResponse,
)
async def create_submenu(
    menu_id: UUID4,
    submenu_data: schemas.SubmenuCreate,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenu_entity = await submenu.create(submenu_data, menu_id)
    return jsonable_encoder(submenu_entity)


@router.patch(
    path='/{submenu_id}',
    status_code=status.HTTP_200_OK,
)
async def patch_submenu(
    menu_id: UUID4,
    submenu_id: UUID4,
    submenu_data: schemas.SubmenuUpdate,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    submenu_entity = await submenu.update(submenu_data, submenu_id, menu_id)
    return jsonable_encoder(submenu_entity)


@router.delete(
    path='/{submenu_id}',
    status_code=status.HTTP_200_OK,
)
async def delete_submenu(
    background_tasks: BackgroundTasks,
    menu_id: UUID4,
    submenu_id: UUID4,
    submenu: SubmenuService = Depends(),
) -> JSONResponse:
    background_tasks.add_task(submenu.clear_cache, submenu_id, menu_id)
    await submenu.delete(submenu_id, menu_id)
