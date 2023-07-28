from fastapi import Depends, APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.submenus import crud, schemas
from src.dependencies import get_session

router = APIRouter(prefix="/api/v1/menus")

@router.get(
    path="/{menu_id}/submenus", 
    status_code=status.HTTP_200_OK,
    tags=["Submenus"],
)
async def list_menu_submenu(
    menu_id: UUID4, 
    session: AsyncSession=Depends(get_session),
) -> JSONResponse:
    submenus = await crud.list_menu_submenu(menu_id, session)
    return jsonable_encoder(submenus)


@router.get(
    path="/{menu_id}/submenus/{submenu_id}",
    status_code=status.HTTP_200_OK,
    tags=["Submenus"],
)
async def get_submenu(
    submenu_id: UUID4, 
    response: Response, 
    session: AsyncSession=Depends(get_session)
) -> JSONResponse:
    submenu = await crud.get_submenu(session, submenu_id)

    if not submenu:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return jsonable_encoder(submenu)


@router.post(
    path="/{menu_id}/submenus", 
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.SubmenuCreateResponse,
    tags=["Submenus"],
)
async def post_menu_submenu(
    menu_id: UUID4, 
    submenu: schemas.SubmenuCreate, 
    session: AsyncSession=Depends(get_session)
) -> JSONResponse:
    submenu = await crud.create_menu_submenu(session, submenu, menu_id)
    return jsonable_encoder(submenu)


@router.patch(
    path="/{menu_id}/submenus/{submenu_id}", 
    status_code=status.HTTP_200_OK,
    tags=["Submenus"],
)
async def patch_submenu(
    submenu_id: UUID4, 
    submenu: schemas.SubmenuUpdate, 
    session: AsyncSession=Depends(get_session),
) -> JSONResponse:
    submenu = await crud.update_submenu(session, submenu, submenu_id)
    return jsonable_encoder(submenu)


@router.delete(
    path="/{menu_id}/submenus/{submenu_id}", 
    status_code=status.HTTP_200_OK,
    tags=["Submenus"],
)
async def delete_submenu(
    submenu_id: UUID4, 
    session: AsyncSession=Depends(get_session),
) -> JSONResponse:
    await crud.delete_submenu(session, submenu_id)
