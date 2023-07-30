from fastapi import FastAPI

from src.database import Base
from src.menus.router import router as menu_router
from src.submenus.router import router as submenu_router
from src.dishes.router import router as dish_router


def create_app():
    app = FastAPI()

    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)

    return app


app = create_app()
