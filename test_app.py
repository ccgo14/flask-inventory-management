import pytest
from unittest.mock import patch
import requests
import app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        initial_state = [
            {
                "id": 1,
                "product_name": "Organic Almond Milk",
                "brands": "Silk",
                "ingredients_text": "Filtered water, almonds, cane sugar...",
                "price": 3.99,
                "stock": 45
            },
            {
                "id": 2,
                "product_name": "Whole Wheat Bread",
                "brands": "Baker's Choice",
                "ingredients_text": "Whole wheat flour, water, yeast...",
                "price": 2.49,
                "stock": 20
            }
        ]
        app.INVENTORY.clear()
        app.INVENTORY.extend(initial_state)
        yield client

def test_get_all_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['product_name'] == "Organic Almond Milk"

def test_get_single_item_success(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['product_name'] == "Organic Almond Milk"

def test_get_single_item_not_found(client):
    response = client.get('/inventory/999')
    assert response.status_code == 404

def test_post_new_item_manual(client):
    payload = {
        "product_name": "Greek Yogurt",
        "price": 4.99,
        "stock": 15
    }
    response = client.post('/inventory', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['id'] == 3
    assert data['product_name'] == "Greek Yogurt"

def test_post_new_item_missing_fields(client):
    payload = {
        "price": 4.99
    }
    response = client.post('/inventory', json=payload)
    assert response.status_code == 400

def test_post_new_item_invalid_json(client):
    response = client.post('/inventory', data="not json", content_type="application/json")
    assert response.status_code == 400

@patch('app.requests.get')
def test_post_item_external_api_success(mock_get, client):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Live Rice Noodles",
            "brands": "A Taste of Thai",
            "ingredients_text": "Rice flour, water"
        }
    }

    payload = {
        "barcode": "737628011862",
        "price": 3.49,
        "stock": 10
    }
    response = client.post('/inventory', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['product_name'] == "Live Rice Noodles"
    assert data['brands'] == "A Taste of Thai"

@patch('app.requests.get')
def test_post_item_external_api_fallback(mock_get, client):
    mock_get.side_effect = requests.exceptions.RequestException()

    payload = {
        "barcode": "0000000000",
        "price": 1.00,
        "stock": 5
    }
    response = client.post('/inventory', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['product_name'] == "Fallback Product"
    assert "Could not fetch from OpenFoodFacts API" in data['ingredients_text']

def test_patch_item_success(client):
    payload = {
        "price": 4.25,
        "stock": 40
    }
    response = client.patch('/inventory/1', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['price'] == 4.25
    assert data['stock'] == 40

def test_patch_item_not_found(client):
    payload = {"price": 5.00}
    response = client.patch('/inventory/999', json=payload)
    assert response.status_code == 404

def test_patch_item_invalid_json(client):
    response = client.patch('/inventory/1', data="not json", content_type="application/json")
    assert response.status_code == 400

def test_delete_item_success(client):
    response = client.delete('/inventory/1')
    assert response.status_code == 200
    assert len(app.INVENTORY) == 1

def test_delete_item_not_found(client):
    response = client.delete('/inventory/999')
    assert response.status_code == 404