from fastapi import Depends, APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.menus import crud, schemas
from src.dependencies import get_session
from src.database import Base

router = APIRouter(prefix="/api/v1/menus")


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Menus"],
)
async def list_menu(session: AsyncSession = Depends(get_session)) -> JSONResponse:
    menus = await crud.list_menu(session)
    return jsonable_encoder(
        [schemas.MenuBase(title=m.title, description=m.description) for m in menus]
    )


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Menus"],
)
async def get_menu(
    id: UUID4,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    menu = await crud.get_menu(session, id)

    if not menu:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return jsonable_encoder(menu)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MenuCreateResponse,
    tags=["Menus"],
)
async def post_menu(
    menu: schemas.MenuCreate,
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    menu = await crud.create_menu(session, menu)
    return jsonable_encoder(menu)


@router.patch(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Menus"],
)
async def patch_menu(
    id: UUID4,
    menu: schemas.MenuUpdate,
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    menu = await crud.update_menu(session, menu, id)
    return jsonable_encoder(menu)


@router.delete(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Menus"],
)
async def delete_menu(
    id: UUID4,
    session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    await crud.delete_menu(session, id)
