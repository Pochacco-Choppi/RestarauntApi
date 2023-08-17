import pytest
from httpx import AsyncClient

from src.main import url_for
from tests.data import (
    DISH_DATA_JSON,
    DISH_PATCH_DATA_JSON,
    MENU_DATA_JSON,
    SUBMENU_DATA_JSON,
)

global target_menu_id
target_menu_id = None

global target_submenu_id
target_submenu_id = None

global target_dish_id
target_dish_id = None


@pytest.mark.asyncio
async def test_get_related_is_empty(client: AsyncClient) -> None:
    response = await client.get(
        url_for('list_menu_with_related'),
    )
    assert response.status_code == 200

    assert response.json() == []


@pytest.mark.asyncio
async def test_list_dishes_is_empty(client: AsyncClient) -> None:
    # Create Menu
    response = await client.post(url_for('create_menu'), json=MENU_DATA_JSON)

    global target_menu_id
    target_menu_id = response.json()['id']
    #
    # Create Submenu
    response = await client.post(
        url_for('create_submenu', menu_id=target_menu_id), json=SUBMENU_DATA_JSON
    )
    global target_submenu_id

    target_submenu_id = response.json()['id']
    #

    response = await client.get(
        url_for('create_dish', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_dish(client: AsyncClient) -> None:
    response = await client.post(
        url_for('create_dish', menu_id=target_menu_id, submenu_id=target_submenu_id),
        json=DISH_DATA_JSON,
    )
    assert response.status_code == 201, response.text

    assert response.json()['title'] == DISH_DATA_JSON['title']
    assert response.json()['description'] == DISH_DATA_JSON['description']
    assert response.json()['price'] == DISH_DATA_JSON['price']
    assert 'id' in response.json()
    global target_dish_id

    target_dish_id = response.json()['id']


@pytest.mark.asyncio
async def test_list_dishes_is_not_empty(client: AsyncClient) -> None:
    response = await client.get(
        url_for('list_dish', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_dish(client: AsyncClient) -> None:
    response = await client.get(
        url_for('get_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
    )
    assert response.status_code == 200

    assert response.json()['title'] == DISH_DATA_JSON['title']
    assert response.json()['description'] == DISH_DATA_JSON['description']
    assert response.json()['price'] == DISH_DATA_JSON['price']
    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_patch_dish(client: AsyncClient) -> None:
    response = await client.patch(
        url_for('patch_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
        json=DISH_PATCH_DATA_JSON,
    )
    assert response.status_code == 200

    assert response.json()['title'] == DISH_PATCH_DATA_JSON['title']
    assert response.json()['description'] == DISH_PATCH_DATA_JSON['description']
    assert response.json()['price'] == DISH_PATCH_DATA_JSON['price']
    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_get_related(client: AsyncClient) -> None:
    response = await client.get(
        url_for('list_menu_with_related'),
    )
    assert response.status_code == 200

    assert response.json()[0]['title'] == MENU_DATA_JSON['title']
    assert response.json()[0]['description'] == MENU_DATA_JSON['description']
    assert response.json()[0]['submenus'] != []
    assert response.json()[0]['submenus'][0]['title'] == SUBMENU_DATA_JSON['title']
    assert response.json()[0]['submenus'][0]['description'] == SUBMENU_DATA_JSON['description']
    assert response.json()[0]['submenus'][0]['dishes'] != []
    assert response.json()[0]['submenus'][0]['dishes'][0]['title'] == DISH_PATCH_DATA_JSON['title']
    assert response.json()[0]['submenus'][0]['dishes'][0]['description'] == DISH_PATCH_DATA_JSON['description']
    assert response.json()[0]['submenus'][0]['dishes'][0]['price'] == DISH_PATCH_DATA_JSON['price']


@pytest.mark.asyncio
async def test_delete_dish(client: AsyncClient) -> None:
    response = await client.delete(
        url_for('delete_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
    )

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.asyncio
async def test_get_dish_not_found(client: AsyncClient) -> None:
    response = await client.get(
        url_for('get_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
    )

    assert response.status_code == 404

    # Delete Menu
    response = await client.delete(url_for('delete_menu', menu_id=target_menu_id))
    assert response.status_code == 200
