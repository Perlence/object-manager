from flask.testing import FlaskClient
import pytest

from api import app
from api.object_manager import ObjectManager3


@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client


@pytest.fixture
def restore_manager():
    orig_mgr = app.mgr
    yield
    app.mgr = orig_mgr


def test_free_validation(client: FlaskClient):
    resp = client.post('/objects/0', json={'acquired': False})
    assert resp.status_code == 400
    assert resp.json == {'error': 'object must be a positive nonzero int'}


def test_put_get_free_drop(client: FlaskClient, restore_manager):
    app.mgr = ObjectManager3()

    resp = client.post('/objects/get')
    assert resp.json == {'error': 'the pool is empty'}
    assert resp.status_code == 409

    app.mgr.put_object(1)

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

    resp = client.post('/objects/1', json={'acquired': False})
    assert resp.json == {'object': 1, 'acquired': False}
    assert resp.status_code == 200

    app.mgr.drop_object(1)

    resp = client.post('/objects/get')
    assert resp.json == {'error': 'the pool is empty'}
    assert resp.status_code == 409
