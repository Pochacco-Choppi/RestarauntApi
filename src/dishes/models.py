from decimal import Decimal

from typing_extensions import Annotated

from sqlalchemy import Column, ForeignKey, String, UUID, UniqueConstraint, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

import uuid

from src.database import Base

DECIMAL_NUM_16_2 = Annotated[Decimal, 16]

class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[DECIMAL_NUM_16_2] = mapped_column(Numeric(16, 2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submenus.id", ondelete="CASCADE"))

    submenu: Mapped["Submenu"] = relationship("Submenu", back_populates="dishes")

    __table_args__ = (
        UniqueConstraint("submenu_id", "title", "description", "price"),
        )