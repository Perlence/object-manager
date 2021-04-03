import pytest

from api import app


@pytest.fixture
def restore_manager():
    orig_mgr = app.mgr
    yield
    app.mgr = orig_mgr
