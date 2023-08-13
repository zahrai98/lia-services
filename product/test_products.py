import pytest
import json
import pytest
import pytest
from starlette.testclient import TestClient
from beanie import PydanticObjectId

from app.main import app
from product.service import ProductService



@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client 



def test_home(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello!"}


def test_get_all_product(test_app, monkeypatch):
    test_data = [
        {"name": "something","price":12, "description": "something else", "id": 1},
        {"name": "someone","price":13, "description": "someone else", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(ProductService, "find_all_products", mock_get_all)
    response = test_app.get("/products")
    res = {
            "success": True,
            "result": {
                'product': test_data
            },
            'message': "product successfully created",
        }
    
    assert response.status_code == 200
    assert response.json() == res


def test_create_note(test_app, monkeypatch):
    test_request_payload = {"name": "something", "description": "something else", "price": 10}
    test_response_payload = {"_id": "1", "name": "something", "description": "something else", "price": 10}

    async def mock_post(payload):
        return test_response_payload

    monkeypatch.setattr(ProductService, "create_product", mock_post)
    response = test_app.post("/products", content = json.dumps(test_request_payload),)
    test_request_payload["_id"] = "1"
    res = {
            "success": True,
            "result": {
                'product': test_response_payload
            },
            'message': "product successfully created",
        }

    assert response.status_code == 201
    assert response.json() == res


def test_get_product(test_app, monkeypatch):
    product_id = '64d7da099e1ca05de2086a37'
    test_data =  {"name": "something", "description": "something else", "price": 10}

    async def mock_get(product_id):
        test_data_result = test_data
        test_data_result['_id'] = product_id
        return test_data_result
    
    monkeypatch.setattr(ProductService, "find_one_product", mock_get)
    response = test_app.get(f"/products/{product_id}")
    test_data['_id'] = product_id
    res = {
            "success": True,
            "result": {
                'product': test_data
            },
            'message': "product successfully created",
        }
    
    assert response.status_code == 200
    assert response.json() == res


def test_create_note_invalid_input(test_app, monkeypatch):
    test_request_payload = {"name": "something", "description": "something else", "price": "invalid_price"}  # مقدار نامعتبر برای price
    test_response_payload = {"_id": "1", "name": "something", "description": "something else", "price": 10}

    async def mock_post(payload):
        return test_response_payload

    monkeypatch.setattr(ProductService, "create_product", mock_post)
    response = test_app.post("/products", content=json.dumps(test_request_payload))
    test_request_payload["_id"] = "1"

    res = {
        'success': False, 'errors': [{'message': '1 validation error for Request\nbody -> price\n  value is not a valid float (type=type_error.float)',\
                                    'type': 'ValidationError', 'errorCode': 700, 'details':\
                                    [{'loc': ['body', 'price'], 'msg': 'value is not a valid float', 'type': 'type_error.float'}]}]
    }
    assert response.status_code == 422
    assert response.json() == res


def test_delete_product(test_app, monkeypatch):
    product_id = '64d7da099e1ca05de2086a37'
    _id = PydanticObjectId(product_id)
    test_data = {"title": "something", "description": "something else"}

    async def mock_get(product_id):
        test_data_result = test_data
        test_data_result['_id'] = product_id
        return test_data_result
    
    monkeypatch.setattr(ProductService, "find_one_product", mock_get)

    async def mock_delete(product_id):
        return {"success": True,'message': "product successfully deleted"}

    monkeypatch.setattr(ProductService, "delete_product", mock_delete)
    response = test_app.delete(f"/products/{product_id}")
    res = {
            "success": True,
            'message': "product successfully deleted"
        }
    
    assert response.status_code == 200
    assert response.json() == res


def test_update_product(test_app, monkeypatch):
    product_id = '64d7da099e1ca05de2086a37'
    test_update_data = {"name": "something", "description": "something else", "price": 10}

    async def mock_get(product_id):
        test_data_result = test_update_data
        test_data_result['_id'] = product_id
        return test_data_result
    
    monkeypatch.setattr(ProductService, "find_one_product", mock_get)

    async def mock_put(product_id, update_query):
        return test_update_data

    monkeypatch.setattr(ProductService, "find_one_and_update_product", mock_put)

    response = test_app.put(f"/products/{product_id}", content = json.dumps(test_update_data),)
    test_update_data['_id'] = product_id
    res = {
            "success": True,
            "result": {
                'product': test_update_data
            },
            'message': "product successfully updated",
        }
    
    assert response.status_code == 200
    assert response.json() == res


def test_get_product_wrong_input(test_app, monkeypatch):
    invalid_product_id = 'invalid_id'

    async def mock_get(product_id):
        pass
    
    monkeypatch.setattr(ProductService, "find_one_product", mock_get)
    response = test_app.get(f"/products/{invalid_product_id}")
    res = {
        'success': False, 'errors': [{'message': '2 validation errors for Request\npath -> product_id\n  Id must be of type PydanticObjectId (type=type_error)\npath -> product_id\n  Id must be of type PydanticObjectId (type=type_error)', 'type': 'ValidationError', 'errorCode': 700, 'details': [{'loc': ['path', 'product_id'], 'msg': 'Id must be of type PydanticObjectId', 'type': 'type_error'}, {'loc': ['path', 'product_id'], 'msg': 'Id must be of type PydanticObjectId', 'type': 'type_error'}]}]
    }

    assert response.status_code == 422 
    assert response.json() == res