from sqlalchemy import Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship

import uuid

from src.database import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")
