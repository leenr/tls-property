=============
@tls_property
=============

`@tls_property` is a super-tiny library that will help you write
thread-safe classes.

It's acting like a `@cached_property <https://pypi.org/project/cached-property/>`_,
but value will be cached only for current thread.

Garbage collecting is respected, `@tls_property` won't mess up with it.

.. code-block:: python

    from some_library import NonThreadsafeSuperClient
    from tls_property import tls_property

    class SuperClientWrapper:
        @tls_property
        def nonthreadsafe_client(self) -> NonThreadsafeSuperClient:
            return NonThreadsafeSuperClient()

Also, value reset supported via @tls_property :code:`del` ete:

.. code-block:: python

    client = SuperClientWrapper()
    client.something()
    del client.nonthreadsafe_client
    client.something()
..

Module works on Python == 2.7 and Python ~= 3.4.

Installation
------------
.. code-block:: bash

    pip install tls-property
..

License
-------
Public Domain: `CC0 1.0 Universal <https://creativecommons.org/publicdomain/zero/1.0/>`_.
