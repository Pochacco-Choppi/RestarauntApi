import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

from src.database import SQLALCHEMY_DATABASE_URL, AsyncEngine, DatabaseSessionManager
from src.main import create_app


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    sessionmanager = DatabaseSessionManager()
    sessionmanager.init(SQLALCHEMY_DATABASE_URL + '/postgres_test')

    engine: AsyncEngine = sessionmanager._engine

    async with engine.begin() as conn:
        await sessionmanager.create_all(conn)

    async with AsyncClient(app=app, base_url='http://127.0.0.1:5000') as c:
        yield c


app = create_app()


menu_data_json = {'title': 'My menu 1', 'description': 'My menu description 1'}

submenu_data_json = {'title': 'My submenu 1', 'description': 'My submenu description 1'}

submenu_patch_data_json = {
    'title': 'My updated submenu 1',
    'description': 'My updated submenu description 1',
}

menu_patch_data_json = {
    'title': 'My updated menu 1',
    'description': 'My updated menu description 1',
}

dish_data_json = {
    'title': 'My updated dish 1',
    'description': 'My updated dish description 1',
    'price': '25.53',
}

patch_dish_data_json = {
    'title': 'My updated dish 1222',
    'description': 'My updated dish description 1222',
    'price': '50.50',
}

global target_menu_id
target_menu_id = None

global target_submenu_id
target_submenu_id = None

global target_dish_id
target_dish_id = None


@pytest.mark.asyncio
async def test_get_list_menu_is_empty(client):
    response = await client.get('/api/v1/menus/')

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_menu(client):
    response = await client.post('/api/v1/menus/', json=menu_data_json)

    assert response.status_code == 201
    assert response.json()['title'] == menu_data_json['title']
    assert response.json()['description'] == menu_data_json['description']
    assert 'id' in response.json()
    global target_menu_id

    target_menu_id = response.json()['id']


@pytest.mark.asyncio
async def test_list_submenu_is_empty(client):
    response = await client.get(f'/api/v1/menus/{target_menu_id}/submenus')

    assert response.status_code == 200, response.text
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_submenu(client):
    response = await client.post(
        f'/api/v1/menus/{target_menu_id}/submenus', json=submenu_data_json
    )

    assert response.status_code == 201, response.text
    assert response.json()['title'] == submenu_data_json['title']
    assert response.json()['description'] == submenu_data_json['description']
    assert 'id' in response.json()
    global target_submenu_id

    target_submenu_id = response.json()['id']


@pytest.mark.asyncio
async def test_get_submenu(client):
    response = await client.get(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}'
    )

    assert response.status_code == 200
    assert response.json()['title'] == submenu_data_json['title']
    assert response.json()['description'] == submenu_data_json['description']


@pytest.mark.asyncio
async def test_list_submenu_is_not_empty(client):
    response = await client.get(f'/api/v1/menus/{target_menu_id}/submenus')

    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_patch_submenu(client):
    response = await client.patch(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
        json=submenu_patch_data_json,
    )

    assert response.status_code == 200, response.text
    assert response.json()['title'] == submenu_patch_data_json['title']
    assert response.json()['description'] == submenu_patch_data_json['description']


######
@pytest.mark.asyncio
async def test_list_dishes(client):
    response = await client.get(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    )
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_dish(client):
    response = await client.post(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
        json=dish_data_json,
    )
    assert response.status_code == 201, response.text

    assert response.json()['title'] == dish_data_json['title']
    assert response.json()['description'] == dish_data_json['description']
    assert response.json()['price'] == dish_data_json['price']
    assert 'id' in response.json()
    global target_dish_id

    target_dish_id = response.json()['id']


@pytest.mark.asyncio
async def test_list_dishes_is_not_empty(client):
    response = await client.get(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
    )
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_dish(client):
    response = await client.get(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    )
    assert response.status_code == 200

    assert response.json()['title'] == dish_data_json['title']
    assert response.json()['description'] == dish_data_json['description']
    assert response.json()['price'] == dish_data_json['price']
    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_patch_dish(client):
    response = await client.patch(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
        json=patch_dish_data_json,
    )
    assert response.status_code == 200

    assert response.json()['title'] == patch_dish_data_json['title']
    assert response.json()['description'] == patch_dish_data_json['description']
    assert response.json()['price'] == patch_dish_data_json['price']
    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_delete_dish(client):
    response = await client.delete(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
    )

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.asyncio
async def test_get_submenu_after_update(client):
    response = await client.get(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}'
    )

    assert response.status_code == 200
    assert response.json()['title'] == submenu_patch_data_json['title']
    assert response.json()['description'] == submenu_patch_data_json['description']


@pytest.mark.asyncio
async def test_delete_submenu(client):
    response = await client.delete(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}'
    )

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.asyncio
async def test_list_submenu_is_empty_after_delete(client):
    response = await client.get(f'/api/v1/menus/{target_menu_id}/submenus')

    assert response.status_code == 200, response.json()
    assert response.json() == [], response.json()


@pytest.mark.asyncio
async def test_submenu_not_found_after_delete(client):
    response = await client.get(
        f'/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}'
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_menu_list_is_not_empty(client):
    response = await client.get('/api/v1/menus/')

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert len(response.json()) != []


@pytest.mark.asyncio
async def test_get_menu(client):
    response = await client.get(f'/api/v1/menus/{target_menu_id}')

    assert response.status_code == 200
    assert response.json()['title'] == menu_data_json['title']
    assert response.json()['description'] == menu_data_json['description']


@pytest.mark.asyncio
async def test_patch_menu(client):
    response = await client.patch(
        f'/api/v1/menus/{target_menu_id}', json=menu_patch_data_json
    )

    assert response.status_code == 200
    assert response.json()['title'] == menu_patch_data_json['title']
    assert response.json()['description'] == menu_patch_data_json['description']


@pytest.mark.asyncio
async def test_get_menu_after_update(client):
    response = await client.get(f'/api/v1/menus/{target_menu_id}')

    assert response.status_code == 200
    assert response.json()['title'] == menu_patch_data_json['title']
    assert response.json()['description'] == menu_patch_data_json['description']


@pytest.mark.asyncio
async def test_delete_menu(client):
    response = await client.delete(f'/api/v1/menus/{target_menu_id}')

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_menu_after_delete_is_empty(client):
    response = await client.get('/api/v1/menus/')

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_menu_not_found(client):
    response = await client.get(f'/api/v1/menus/{target_menu_id}')

    assert response.status_code == 404
