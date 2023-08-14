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
async def test_list_dishes_is_empty(client):
    # Create Menu
    response = await client.post(url_for('create_menu'), json=menu_data_json)

    global target_menu_id
    target_menu_id = response.json()['id']
    #
    # Create Submenu
    response = await client.post(
        url_for('create_submenu', menu_id=target_menu_id), json=submenu_data_json
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
async def test_create_dish(client):
    response = await client.post(
        url_for('create_dish', menu_id=target_menu_id, submenu_id=target_submenu_id),
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
        url_for('list_dish', menu_id=target_menu_id, submenu_id=target_submenu_id),
    )
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_dish(client):
    response = await client.get(
        url_for('get_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
    )
    assert response.status_code == 200

    assert response.json()['title'] == dish_data_json['title']
    assert response.json()['description'] == dish_data_json['description']
    assert response.json()['price'] == dish_data_json['price']
    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_patch_dish(client):
    response = await client.patch(
        url_for('patch_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
        json=patch_dish_data_json,
    )
    assert response.status_code == 200

    assert response.json()['title'] == patch_dish_data_json['title']
    assert response.json()['description'] == patch_dish_data_json['description']
    assert response.json()['price'] == patch_dish_data_json['price']
    assert 'id' in response.json()


@pytest.mark.asyncio
async def test_get_related(client):
    response = await client.get(
        url_for('list_menu_with_related'),
    )
    assert response.status_code == 200

    assert response.json()[0]['title'] == menu_data_json['title']
    assert response.json()[0]['description'] == menu_data_json['description']
    assert response.json()[0]['submenus'] != []
    assert response.json()[0]['submenus'][0]['title'] == submenu_data_json['title']
    assert response.json()[0]['submenus'][0]['description'] == submenu_data_json['description']
    assert response.json()[0]['submenus'][0]['dishes'] != []
    assert response.json()[0]['submenus'][0]['dishes'][0]['title'] == patch_dish_data_json['title']
    assert response.json()[0]['submenus'][0]['dishes'][0]['description'] == patch_dish_data_json['description']
    assert response.json()[0]['submenus'][0]['dishes'][0]['price'] == patch_dish_data_json['price']


@pytest.mark.asyncio
async def test_delete_dish(client):
    response = await client.delete(
        url_for('delete_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
    )

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.asyncio
async def test_get_dish_not_found(client):
    response = await client.get(
        url_for('get_dish', menu_id=target_menu_id, submenu_id=target_submenu_id, dish_id=target_dish_id),
    )

    assert response.status_code == 404

    # Delete Menu
    response = await client.delete(url_for('delete_menu', menu_id=target_menu_id))
    assert response.status_code == 200
