import asyncio

from celery import Celery
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from src.admin.utils import get_entitues_from_excel
from src.config import RABBITMQ_HOST
from src.database import async_session
from src.dishes.models import Dish
from src.menus.models import Menu
from src.submenus.models import Submenu

broker_url = f'amqp://{RABBITMQ_HOST}'

celery = Celery(__name__, broker=broker_url)


async def bulk_create() -> None:
    menus = get_entitues_from_excel()
    session = async_session()

    if not menus:
        await session.execute(delete(Menu))
        await session.commit()
        return

    menus_to_add = []
    menus_to_add_id = []

    submenus_to_add = []
    submenus_to_add_id = []

    dishes_to_add = []
    dishes_to_add_id = []

    for menu in menus:
        menu_submenus = menu.pop('submenus')
        menus_to_add.append(menu)
        menus_to_add_id.append(menu['id'])

        for submenu in menu_submenus:
            submenu_dishes = submenu.pop('dishes')
            submenus_to_add.append(submenu)
            submenus_to_add_id.append(submenu['id'])

            for dish in submenu_dishes:
                dishes_to_add.append(dish)
                dishes_to_add_id.append(dish['id'])

        for menu in menus_to_add:
            insert_stmt = insert(Menu).values(menu)
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=['id'],
                                                               set_=menu)

            await session.execute(
                statement=do_update_stmt,
            )

        for submenu in submenus_to_add:
            insert_stmt = insert(Submenu).values(submenu)
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=['id'],
                                                               set_=submenu)
            await session.execute(
                statement=do_update_stmt
            )

        for dish in dishes_to_add:
            insert_stmt = insert(Dish).values(dish)
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=['id'],
                                                               set_=dish)
            await session.execute(
                statement=do_update_stmt
            )

        delete_menu_stmt = delete(Menu).where(Menu.id.not_in(menus_to_add_id))
        await session.execute(delete_menu_stmt)
        delete_submenu_stmt = delete(Submenu).where(Submenu.id.not_in(submenus_to_add_id))
        await session.execute(delete_submenu_stmt)
        delete_dish_stmt = delete(Dish).where(Dish.id.not_in(dishes_to_add_id))
        await session.execute(delete_dish_stmt)

        await session.commit()


@celery.task
def test():
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(bulk_create())
    except Exception:
        if not loop.is_closed:
            loop.close()


celery.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'src.celery_worker.test',
        'schedule': 15.0
    }
}
