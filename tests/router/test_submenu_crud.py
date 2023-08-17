import pytest
from httpx import AsyncClient

from src.main import url_for
from tests.data import MENU_DATA_JSON, SUBMENU_DATA_JSON, SUBMENU_PATCH_DATA_JSON

global target_menu_id
target_menu_id = None

global target_submenu_id
target_submenu_id = None


@pytest.mark.asyncio
async def test_list_submenu_is_empty(client: AsyncClient) -> None:
    # Create Menu
    response = await client.post(url_for('create_menu'), json=MENU_DATA_JSON)

    global target_menu_id
    target_menu_id = response.json()['id']
    #

    response = await client.get(url_for('list_submenu', menu_id=target_menu_id))

    assert response.status_code == 200, response.text
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_submenu(client: AsyncClient) -> None:
    response = await client.post(
        url_for('create_submenu', menu_id=target_menu_id), json=SUBMENU_DATA_JSON
    )

    assert response.status_code == 201, response.text
    assert response.json()['title'] == SUBMENU_DATA_JSON['title']
    assert response.json()['description'] == SUBMENU_DATA_JSON['description']
    assert 'id' in response.json()
    global target_submenu_id

    target_submenu_id = response.json()['id']


@pytest.mark.asyncio
async def test_list_submenu_is_not_empty(client: AsyncClient) -> None:
    response = await client.get(url_for('list_submenu', menu_id=target_menu_id))

    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_submenu(client: AsyncClient) -> None:
    response = await client.get(
        url_for('get_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 200
    assert response.json()['title'] == SUBMENU_DATA_JSON['title']
    assert response.json()['description'] == SUBMENU_DATA_JSON['description']


@pytest.mark.asyncio
async def test_patch_submenu(client: AsyncClient) -> None:
    response = await client.patch(
        url_for('patch_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
        json=SUBMENU_PATCH_DATA_JSON,
    )

    assert response.status_code == 200, response.text
    assert response.json()['title'] == SUBMENU_PATCH_DATA_JSON['title']
    assert response.json()['description'] == SUBMENU_PATCH_DATA_JSON['description']


@pytest.mark.asyncio
async def test_get_submenu_after_update(client: AsyncClient) -> None:
    response = await client.get(
        url_for('get_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 200
    assert response.json()['title'] == SUBMENU_PATCH_DATA_JSON['title']
    assert response.json()['description'] == SUBMENU_PATCH_DATA_JSON['description']


@pytest.mark.asyncio
async def test_delete_submenu(client: AsyncClient) -> None:
    response = await client.delete(
        url_for('delete_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.asyncio
async def test_list_submenu_is_empty_after_delete(client: AsyncClient) -> None:
    response = await client.get(
        url_for('list_submenu', menu_id=target_menu_id),
    )

    assert response.status_code == 200, response.json()
    assert response.json() == [], response.json()


@pytest.mark.asyncio
async def test_get_submenu_not_found(client: AsyncClient) -> None:
    response = await client.get(
        url_for('get_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 404

    # delete Menu
    response = await client.delete(url_for('delete_menu', menu_id=target_menu_id))
    assert response.status_code == 200
