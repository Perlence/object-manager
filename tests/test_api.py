from flask.testing import FlaskClient
import pytest

from api.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_put_validation(client: FlaskClient):
    resp = client.post('/objects', json={})
    assert resp.status_code == 400
    assert resp.json == {'error': 'missing key "object"'}

    resp = client.post('/objects', json={'object': 'beep'})
    assert resp.status_code == 400
    assert resp.json == {'error': 'object must be an int'}

    resp = client.post('/objects', json={'object': 0})
    assert resp.status_code == 400
    assert resp.json == {'error': 'object must be a positive nonzero int'}


def test_put_get_free_drop(client: FlaskClient):
    resp = client.post('/objects/get')
    assert resp.json == {'error': 'the pool is empty'}
    assert resp.status_code == 409

    resp = client.delete('/objects/1')
    assert resp.json == {'object': 1, 'acquired': False, 'deleted': True}
    assert resp.status_code == 404

    resp = client.post('/objects', json={'object': 1})
    assert resp.json == {'object': 1, 'acquired': False}
    assert resp.status_code == 201
    resp = client.post('/objects', json={'object': 1})
    assert resp.json == {'object': 1, 'acquired': False}
    assert resp.status_code == 200

    resp = client.post('/objects/1', json={})
    assert resp.status_code == 400
    assert resp.json == {'error': 'missing key "acquired"'}
    resp = client.post('/objects/1', json={'acquired': True})
    assert resp.json == {'error': 'cannot acquire a particular object'}
    assert resp.status_code == 400
    resp = client.post('/objects/1', json={'acquired': False})
    assert resp.json == {'object': 1, 'acquired': False}
    assert resp.status_code == 200

    resp = client.post('/objects/get')
    assert resp.json == {'object': 1, 'acquired': True}
    assert resp.status_code == 200

    resp = client.post('/objects/get')
    assert resp.json == {'error': 'all objects are acquired'}
    assert resp.status_code == 409

    resp = client.delete('/objects/1')
    assert resp.json == {'error': 'cannot drop an acquired object'}
    assert resp.status_code == 409

    resp = client.post('/objects/1', json={'acquired': False})
    assert resp.json == {'object': 1, 'acquired': False}
    assert resp.status_code == 200

    resp = client.delete('/objects/1')
    assert resp.json == {'object': 1, 'acquired': False, 'deleted': True}
    assert resp.status_code == 200

    resp = client.post('/objects/get')
    assert resp.json == {'error': 'the pool is empty'}
    assert resp.status_code == 409
