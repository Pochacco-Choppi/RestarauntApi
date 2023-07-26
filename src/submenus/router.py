from fastapi import Depends, APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session

from src.submenus import crud, schemas
from src.dependencies import get_db

router = APIRouter(prefix="/api/v1/menus")

@router.get("/{menu_id}/submenus", status_code=status.HTTP_200_OK)
async def list_menu_submenu(menu_id: UUID4, db: Session=Depends(get_db)):
    submenus = crud.list_menu_submenu(menu_id, db)
    return jsonable_encoder(submenus)


@router.get("/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
async def get_submenu(submenu_id: UUID4, response: Response, db: Session=Depends(get_db)):
    submenu = crud.get_submenu(db, submenu_id)

    if not submenu:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    submenu.dishes_count = len(submenu.dishes)
    return jsonable_encoder(submenu)


@router.post("/{menu_id}/submenus", status_code=status.HTTP_201_CREATED)
async def post_menu_submenu(menu_id: UUID4, submenu: schemas.SubmenuCreate, db: Session=Depends(get_db)):
    submenu = crud.create_menu_submenu(db, submenu, menu_id)
    return jsonable_encoder(submenu)


@router.patch("/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
async def patch_submenu(submenu_id: UUID4, submenu: schemas.SubmenuUpdate, db: Session=Depends(get_db)):
    submenu = crud.update_submenu(db, submenu, submenu_id)
    return jsonable_encoder(submenu)


@router.delete("/{menu_id}/submenus/{submenu_id}", status_code=status.HTTP_200_OK)
async def delete_submenu(submenu_id: UUID4, db: Session=Depends(get_db)):
    crud.delete_submenu(db, submenu_id)