from sqlalchemy import Column, ForeignKey, String, UUID, UniqueConstraint, DECIMAL
from sqlalchemy.orm import relationship

import uuid

from src.database import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(DECIMAL(precision=16,scale=2))
    submenu_id = Column(UUID, ForeignKey("submenus.id", ondelete="CASCADE"))

    submenu = relationship("Submenu", back_populates="dishes")

    __table_args__ = (
        UniqueConstraint("submenu_id", "title", "description", "price"),
        )