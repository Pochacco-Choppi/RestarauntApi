from sqlalchemy.orm import Session
from pydantic import UUID4

from src.menus.models import Menu
from src.menus.schemas import MenuCreate, MenuUpdate
from src.dependencies import get_db

def get_menu(db: Session, menu_id: UUID4):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    return db_menu

def list_menu(db: Session, skip: int = 0, limit: int = 100):
    db_menus = db.query(Menu).offset(skip).limit(limit).all()
    return db_menus

def create_menu(db: Session, menu: MenuCreate):
    db_menu = Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def update_menu(db: Session, menu: MenuUpdate, menu_id: UUID4):
    # menu = get_menu(db, menu_id)
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

def delete_menu(db: Session, menu_id: UUID4):
    # menu = get_menu(db, menu_id)
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    db.delete(db_menu)
    db.commit()
