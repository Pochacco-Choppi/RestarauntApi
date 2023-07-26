from sqlalchemy.orm import Session
from pydantic import UUID4

from .models import Dish
from .schemas import DishCreate, DishUpdate


def get_dish(db: Session, dish_id: UUID4):
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    return db_dish

def list_submenu_dish(submenu_id: UUID4, db: Session, skip: int = 0, limit: int = 100):
    db_dishs = db.query(Dish).filter(Dish.submenu_id == submenu_id).offset(skip).limit(limit).all()
    return db_dishs

def update_dish(db: Session, dish: DishUpdate, dish_id: UUID4):
    # dish = get_dish(db, dish_id)
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    dish_data = dish.dict(exclude_unset=True)
    for key, value in dish_data.items():
        setattr(db_dish, key, value)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish

def delete_dish(db: Session, dish_id: UUID4):
    # dish = get_dish(db, dish_id)
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    db.delete(db_dish)
    db.commit()

def create_submenu_dish(db: Session, dish: DishCreate, submenu_id: UUID4):
    db_dish = Dish(**dish.dict(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish
