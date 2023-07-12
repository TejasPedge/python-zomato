import pytest
import json
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_menu(client):
    response = client.get('/menu')
    assert response.status_code == 200
    menu = json.loads(response.data)
    assert isinstance(menu, list)
    assert len(menu) > 0

def test_add_dish(client):
    dish = {'name': 'Test Dish', 'price': 9.99}
    response = client.post('/menu', json=dish)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Dish added successfully'

def test_remove_dish(client):
    # Assuming the dish with _id = 'dish_id_to_remove' exists
    dish_id = 'dish_id_to_remove'
    response = client.delete(f'/menu/{dish_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Dish removed successfully'

def test_update_dish_availability(client):
    # Assuming the dish with _id = 'dish_id_to_update' exists
    dish_id = 'dish_id_to_update'
    availability_update = {'availability': 'no'}
    response = client.patch(f'/menu/{dish_id}', json=availability_update)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Dish availability updated'

def test_place_order(client):
    order = {'customer_name': 'John Doe', 'dish_ids': ['dish_id_1', 'dish_id_2']}
    response = client.post('/orders', json=order)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Order placed successfully'

def test_update_order_status(client):
    # Assuming the order with order_id = 'order_id_to_update' exists
    order_id = 'order_id_to_update'
    status_update = {'status': 'delivered'}
    response = client.patch(f'/orders/{order_id}', json=status_update)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Order status updated'
