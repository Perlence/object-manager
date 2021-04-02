import threading
from collections import deque


class ObjectManager3:
    def __init__(self):
        self._lock = threading.RLock()
        self._pool = deque()
        self._acquired = deque()

    def put_object(self, obj: int, acquire=False):
        self._validate(obj)
        with self._lock:
            if obj in self._pool or obj in self._acquired:
                return False
            if acquire:
                self._acquired.append(obj)
            else:
                self._pool.append(obj)
            return True

    def get_object(self):
        with self._lock:
            if not self._pool:
                if not self._acquired:
                    raise Conflict('the pool is empty')
                raise Conflict('all objects are acquired')

            obj = self._pool.popleft()
            self._acquired.append(obj)
            return obj

    def free_object(self, obj: int):
        self._validate(obj)
        with self._lock:
            try:
                self._acquired.remove(obj)
            except ValueError:
                if obj not in self._pool:
                    raise Conflict("object is not in the pool") from None
                return False

            self._pool.append(obj)
            return True

    def drop_object(self, obj: int):
        with self._lock:
            if obj in self._acquired:
                raise Conflict('cannot drop an acquired object')

            try:
                self._pool.remove(obj)
                return True
            except ValueError:
                return False

    def _validate(self, obj):
        if not isinstance(obj, int):
            raise TypeError('object must be an int')
        if obj < 1:
            raise ValueError('object must be a positive nonzero int')


class Conflict(Exception):
    pass
