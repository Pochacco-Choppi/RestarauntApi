from fastapi import FastAPI

from src.dishes.router import router as dish_router
from src.menus.router import router as menu_router
from src.submenus.router import router as submenu_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)

    return app


app = create_app()


def url_for(view_name: str, **kwargs) -> str:
    return app.url_path_for(view_name, **kwargs)
