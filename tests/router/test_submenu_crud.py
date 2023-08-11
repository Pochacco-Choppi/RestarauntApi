import pytest

from src.main import url_for

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

global target_menu_id
target_menu_id = None

global target_submenu_id
target_submenu_id = None


@pytest.mark.asyncio
async def test_list_submenu_is_empty(client):
    # Create Menu
    response = await client.post(url_for('create_menu'), json=menu_data_json)

    global target_menu_id
    target_menu_id = response.json()['id']
    #

    response = await client.get(url_for('list_submenu', menu_id=target_menu_id))

    assert response.status_code == 200, response.text
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_submenu(client):
    response = await client.post(
        url_for('create_submenu', menu_id=target_menu_id), json=submenu_data_json
    )

    assert response.status_code == 201, response.text
    assert response.json()['title'] == submenu_data_json['title']
    assert response.json()['description'] == submenu_data_json['description']
    assert 'id' in response.json()
    global target_submenu_id

    target_submenu_id = response.json()['id']


@pytest.mark.asyncio
async def test_list_submenu_is_not_empty(client):
    response = await client.get(url_for('list_submenu', menu_id=target_menu_id))

    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_submenu(client):
    response = await client.get(
        url_for('get_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 200
    assert response.json()['title'] == submenu_data_json['title']
    assert response.json()['description'] == submenu_data_json['description']


@pytest.mark.asyncio
async def test_patch_submenu(client):
    response = await client.patch(
        url_for('patch_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
        json=submenu_patch_data_json,
    )

    assert response.status_code == 200, response.text
    assert response.json()['title'] == submenu_patch_data_json['title']
    assert response.json()['description'] == submenu_patch_data_json['description']


@pytest.mark.asyncio
async def test_get_submenu_after_update(client):
    response = await client.get(
        url_for('get_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 200
    assert response.json()['title'] == submenu_patch_data_json['title']
    assert response.json()['description'] == submenu_patch_data_json['description']


@pytest.mark.asyncio
async def test_delete_submenu(client):
    response = await client.delete(
        url_for('delete_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.asyncio
async def test_list_submenu_is_empty_after_delete(client):
    response = await client.get(
        url_for('list_submenu', menu_id=target_menu_id),
    )

    assert response.status_code == 200, response.json()
    assert response.json() == [], response.json()


@pytest.mark.asyncio
async def test_get_submenu_not_found(client):
    response = await client.get(
        url_for('get_submenu', menu_id=target_menu_id, submenu_id=target_submenu_id),    
    )

    assert response.status_code == 404

    # delete Menu
    response = await client.delete(url_for('delete_menu', menu_id=target_menu_id))
    assert response.status_code == 200
