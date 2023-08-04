from typing import Optional

from sqlalchemy import String, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

import uuid

from src.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    submenus: Mapped[list["Submenu"]] = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )
