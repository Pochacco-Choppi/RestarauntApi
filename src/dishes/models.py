import uuid

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.dishes.constants import DECIMAL_NUM_16_2


class Dish(Base):
    __tablename__ = 'dishes'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[DECIMAL_NUM_16_2] = mapped_column(Numeric(16, 2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('submenus.id', ondelete='CASCADE')
    )

    submenu: Mapped['Submenu'] = relationship('Submenu', back_populates='dishes')

    __table_args__ = (UniqueConstraint('submenu_id', 'title', 'description', 'price'),)
