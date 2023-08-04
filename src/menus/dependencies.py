from typing import Mapping

from pydantic import UUID4

from src.menus import crud


async def valid_menu_id(menu_id: UUID4) -> Mapping:
    menu = await crud.get_menu(id=post_id)
    if not menu:
        raise ValueError()
        # raise MenuNotFound()

    return menu
