from sqlalchemy.orm import Session

from .models import Submenu
from .schemas import SubmenuCreate, SubmenuUpdate

def get_submenu(db: Session, submenu_id: str):
    db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    return db_submenu

def list_menu_submenu(menu_id: str, db: Session, skip: int = 0, limit: int = 100):
    db_submenus = db.query(Submenu).filter(Submenu.menu_id == menu_id).offset(skip).limit(limit).all()
    return db_submenus

def create_menu_submenu(db: Session, submenu: SubmenuCreate, menu_id: str):
    db_submenu = Submenu(**submenu.dict(), menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

def update_submenu(db: Session, submenu: SubmenuUpdate, submenu_id: str):
    # submenu = get_submenu(db, submenu_id)
    db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    submenu_data = submenu.dict(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(db_submenu, key, value)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu

def delete_submenu(db: Session, submenu_id: str):
    # submenu = get_submenu(db, submenu_id)
    db_submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    db.delete(db_submenu)
    db.commit()
