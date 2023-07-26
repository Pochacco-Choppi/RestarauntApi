from fastapi import Depends, APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session

from src.menus import crud, schemas
from src.dependencies import get_db

router = APIRouter(prefix="/api/v1/menus")


@router.get("/", status_code=status.HTTP_200_OK)
async def list_menu(db: Session=Depends(get_db)):
    menus = crud.list_menu(db)
    return menus

@router.get("/{id}", status_code=status.HTTP_200_OK)
# Need to think about it
async def get_menu(id: UUID4, response: Response, db: Session=Depends(get_db)):
    menu = crud.get_menu(db, id)

    if not menu:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    menu.submenus_count = len(menu.submenus)
    menu.dishes_count = sum([len(submenu.dishes) for submenu in menu.submenus])
    return jsonable_encoder(menu)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_menu(menu: schemas.MenuCreate, db: Session=Depends(get_db)):
    menu = crud.create_menu(db, menu)
    return jsonable_encoder(menu)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def patch_menu(id: UUID4, menu: schemas.MenuUpdate, db: Session=Depends(get_db)):
    menu = crud.update_menu(db, menu, id)
    return jsonable_encoder(menu)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_menu(id: UUID4, db: Session=Depends(get_db)):
    crud.delete_menu(db, id)
