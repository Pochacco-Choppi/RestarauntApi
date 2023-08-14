import os
import time

import asyncio

from celery import Celery
from fastapi import Depends
import requests

from typing import Any

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy import and_, func, select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRedisCacheRepository
from src.dependencies import get_session
from src.dishes.models import Dish
from src.menus.models import Menu
from src.menus.schemas import MenuCreate, MenuUpdate, Menu as MenuSchema
from src.submenus.models import Submenu
from src.dishes.models import Dish
from src.database import async_session, session_manager
from src.admin.utils import get_entitues_from_excel
import asyncio

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
import os
import json
from pprint import pprint
from fastapi.encoders import jsonable_encoder
import contextlib

import pandas as pd

excel_file_path = 'src/admin/Menu.xlsx'

rabbitmq_host = os.environ['RABBITMQ_HOST']
redis_host = os.environ['REDIS_HOST']


broker_url = f"amqp://{rabbitmq_host}"

redis_url = f'redis://{redis_host}'
celery = Celery(__name__, broker=broker_url, backend=redis_url)

async def bulk_create():
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
        # db_menu = MenuSchema(**menu)
        menu_submenus = menu.pop("submenus")
        menus_to_add.append(menu)
        menus_to_add_id.append(menu["id"])

        for submenu in menu_submenus:
            submenu_dishes = submenu.pop("dishes")
            submenus_to_add.append(submenu)
            submenus_to_add_id.append(submenu["id"])
                
            for dish in submenu_dishes:
                dishes_to_add.append(dish)
                dishes_to_add_id.append(dish["id"])
                    
        for menu in menus_to_add:
            insert_stmt = insert(Menu).values(menu)
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=["id"],
        set_=menu)

            await session.execute(
                statement=do_update_stmt,
            )
            
        for submenu in submenus_to_add:
            insert_stmt = insert(Submenu).values(submenu)
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=["id"],
        set_=submenu)
            await session.execute(
                statement=do_update_stmt
            )

        for dish in dishes_to_add:
            insert_stmt = insert(Dish).values(dish)
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=["id"],
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
    except:
        if not loop.is_closed:
            loop.close()


celery.conf.beat_schedule = {
 "run-me-every-ten-seconds": {
 "task": "src.celery_worker.test",
 "schedule": 15.0
 }
}
