import pytest

from api.object_manager import Conflict, ObjectManager3


class TestObjectManager3:
    def test_put_validation(self):
        mgr = ObjectManager3()
        with pytest.raises(TypeError, match='must be an int'):
            mgr.put_object(None)
        with pytest.raises(ValueError, match='must be a positive nonzero int'):
            mgr.put_object(0)

    def test_put_get_free_drop(self):
        mgr = ObjectManager3()

        assert mgr.list_objects() == ((), ())
        with pytest.raises(Conflict, match='the pool is empty'):
            mgr.get_object()
        assert mgr.drop_object(1) is False

        assert mgr.put_object(1) is True
        assert mgr.put_object(1) is False
        assert mgr.list_objects() == ((1,), ())

        assert mgr.free_object(1) is False

        assert mgr.get_object() == 1
        assert mgr.list_objects() == ((), (1,))

        with pytest.raises(Conflict, match='all objects are acquired'):
            mgr.get_object()
        with pytest.raises(Conflict, match='cannot drop an acquired object'):
            mgr.drop_object(1)

        assert mgr.free_object(1) is True
        assert mgr.list_objects() == ((1,), ())
        assert mgr.drop_object(1) is True
        assert mgr.list_objects() == ((), ())

        with pytest.raises(Conflict, match='the pool is empty'):
            mgr.get_object()
