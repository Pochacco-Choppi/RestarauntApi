from sqlalchemy import Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

import uuid

from src.database import Base

class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(UUID, ForeignKey("menus.id", ondelete="CASCADE"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")
