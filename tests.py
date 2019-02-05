import gc
import random
import sys
import threading
import weakref
from functools import partial
from itertools import product
from time import sleep

import pytest

from tls_property import tls_property


if sys.version_info >= (3,):  # Python 3.x and above
    create_daemon_thread = partial(threading.Thread, daemon=True)

    get_thread_ident = threading.get_ident

else:  # Python 2.7 and below
    def create_daemon_thread(**kwargs):
        thread = threading.Thread(**kwargs)
        thread.daemon = True
        return thread

    import thread
    get_thread_ident = thread.get_ident


@pytest.fixture
def cls():
    # tuples doesn't support weak references "even when subclassed"
    #  (according to the documentation of weakref module)
    class Result:
        def __init__(self, thread_ident, i):
            self.thread_ident = thread_ident
            self.i = i

    class Test:
        def __init__(self):
            self.tls = threading.local()

        def _prop(self):
            i = getattr(self.tls, 'i', 0)
            setattr(self.tls, 'i', i + 1)
            return Result(get_thread_ident(), i)

        prop = tls_property(_prop)

    return Test


def test_tls_property_fixture(cls):
    obj = cls()
    for i in range(20):
        p = obj._prop()
        assert p.thread_ident == get_thread_ident()
        assert p.i == i, 'i not increasing'


def test_tls_property_once(cls):
    objs = [cls() for _ in range(100)]
    rounds = list(product(objs, range(20)))
    random.shuffle(rounds)
    for obj, _ in rounds:
        p = obj.prop
        assert p
        assert p.i == 0, 'Function under @tls_property ' \
                         'was called more than once'


def test_tls_property_threading(cls):
    exceptions = []
    obj = cls()

    def target():
        try:
            for i in range(20):
                assert obj.prop.thread_ident == get_thread_ident(), \
                    'Value created in another thread'
                sleep(random.random() / 10)
        except Exception as exc:
            exceptions.append(exc)

    threads = []
    for _ in range(10):
        thread = create_daemon_thread(target=target)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    for exc in exceptions:
        raise exc


def test_tls_property_gc(cls):
    obj = cls()
    obj_ref = weakref.ref(obj)

    p = obj.prop
    assert p
    p_ref = weakref.ref(p)

    del p, obj
    gc.collect()

    assert obj_ref() is None, 'Object is still alive?!'
    assert p_ref() is None, 'Value is still alive'


def test_tls_property_get(cls):
    assert isinstance(cls.prop, tls_property)
