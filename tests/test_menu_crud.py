import pytest

menu_data_json = {'title': 'My menu 1', 'description': 'My menu description 1'}

menu_patch_data_json = {
    'title': 'My updated menu 1',
    'description': 'My updated menu description 1',
}

global target_menu_id
target_menu_id = None

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
