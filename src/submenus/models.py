import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Submenu(Base):
    __tablename__ = 'submenus'

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    menu_id: Mapped[uuid] = mapped_column(ForeignKey('menus.id', ondelete='CASCADE'))

    menu: Mapped['Menu'] = relationship('Menu', back_populates='submenus')
    dishes: Mapped[list['Dish']] = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete-orphan',
        # lazy='joined',
    )
