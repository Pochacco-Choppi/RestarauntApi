import pytest
from httpx import AsyncClient

from src.main import url_for
from tests.data import MENU_DATA_JSON, MENU_PATCH_DATA_JSON

global target_menu_id
target_menu_id = None


@pytest.mark.asyncio
async def test_get_list_menu_is_empty(client: AsyncClient) -> None:
    response = await client.get(url_for('list_menu'))

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_menu(client: AsyncClient) -> None:
    response = await client.post(url_for('create_menu'), json=MENU_DATA_JSON)

    assert response.status_code == 201
    assert response.json()['title'] == MENU_DATA_JSON['title']
    assert response.json()['description'] == MENU_DATA_JSON['description']
    assert 'id' in response.json()
    global target_menu_id

    target_menu_id = response.json()['id']


@pytest.mark.asyncio
async def test_get_menu_list_is_not_empty(client: AsyncClient) -> None:
    response = await client.get(url_for('list_menu'))

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert len(response.json()) != []


@pytest.mark.asyncio
async def test_get_menu(client: AsyncClient) -> None:
    response = await client.get(url_for('get_menu', menu_id=target_menu_id))

    assert response.status_code == 200
    assert response.json()['title'] == MENU_DATA_JSON['title']
    assert response.json()['description'] == MENU_DATA_JSON['description']


@pytest.mark.asyncio
async def test_patch_menu(client: AsyncClient) -> None:
    response = await client.patch(
        url_for('patch_menu', menu_id=target_menu_id),
        json=MENU_PATCH_DATA_JSON,
    )

    assert response.status_code == 200
    assert response.json()['title'] == MENU_PATCH_DATA_JSON['title']
    assert response.json()['description'] == MENU_PATCH_DATA_JSON['description']


@pytest.mark.asyncio
async def test_get_menu_after_update(client: AsyncClient) -> None:
    response = await client.get(url_for('get_menu', menu_id=target_menu_id))

    assert response.status_code == 200
    assert response.json()['title'] == MENU_PATCH_DATA_JSON['title']
    assert response.json()['description'] == MENU_PATCH_DATA_JSON['description']


@pytest.mark.asyncio
async def test_delete_menu(client: AsyncClient) -> None:
    response = await client.delete(url_for('delete_menu', menu_id=target_menu_id))

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_menu_after_delete_is_empty(client: AsyncClient) -> None:
    response = await client.get(url_for('list_menu'))

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_menu_not_found(client: AsyncClient) -> None:
    response = await client.get(url_for('get_menu', menu_id=target_menu_id))

    assert response.status_code == 404
