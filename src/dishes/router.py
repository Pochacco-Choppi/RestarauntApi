from decimal import Decimal

from fastapi import Depends, APIRouter, status, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.dishes import crud, schemas
from src.dependencies import get_db

router = APIRouter(prefix="/api/v1/menus")

@router.get("/{menu_id}/submenus/{submenu_id}/dishes", status_code=status.HTTP_200_OK)
async def list_submenu_dishes(submenu_id: str, db: Session=Depends(get_db)):
    dishes = crud.list_submenu_dish(submenu_id, db)
    return jsonable_encoder(dishes)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=status.HTTP_200_OK)
async def get_dish(dish_id: str, response: Response, db: Session=Depends(get_db)):
    dish = crud.get_dish(db, dish_id)

    if not dish:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
            
    return jsonable_encoder(dish, custom_encoder={Decimal: str,
    float: str})


@router.post("/{menu_id}/submenus/{submenu_id}/dishes", status_code=status.HTTP_201_CREATED)
async def post_submenu_dish(submenu_id: str, dish: schemas.DishCreate, db: Session=Depends(get_db)):
    dish = crud.create_submenu_dish(db, dish, submenu_id)
    return jsonable_encoder(dish, custom_encoder={Decimal: str,
    float: str})


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=status.HTTP_200_OK)
async def patch_dish(dish_id: str, dish: schemas.DishUpdate, db: Session=Depends(get_db)):
    dish = crud.update_dish(db, dish, dish_id)
    return jsonable_encoder(dish, custom_encoder={Decimal: str,
    float: str})

@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", status_code=status.HTTP_200_OK)
async def delete_dish(dish_id: str, db: Session=Depends(get_db)):
    crud.delete_dish(db, dish_id)