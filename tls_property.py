from functools import wraps
from threading import local
from weakref import WeakKeyDictionary


_SENTINEL = object()


class tls_property(object):
    def __init__(self, func):
        wraps(func, updated=())(self)
        self.func = func
        self.tls = local()

    def __get__(self, obj, cls):
        if obj is None:
            return self

        if not hasattr(self.tls, 'container'):
            self.tls.container = WeakKeyDictionary()
            value = _SENTINEL
        else:
            value = self.tls.container.get(obj, _SENTINEL)

        if value is _SENTINEL:
            value = self.func(obj)
            self.tls.container[obj] = value

        return value


__all__ = ('tls_property',)
