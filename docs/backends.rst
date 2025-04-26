Backend Types
============

StatefulPy supports different backend types for state persistence, each with their own strengths:

SQLite Backend
-------------

The SQLite backend stores state in a local SQLite database file. It's best suited for:

* Single-process applications
* Local development and testing
* Scenarios where no external dependencies are desired

Configuration options:

* ``db_path``: Path to SQLite database file (default: ``"statefulpy.db"``)
* ``serializer``: Serialization format (``"pickle"`` or ``"json"``)

Example:

.. code-block:: python

   @stateful(backend="sqlite", db_path="app_state.db", serializer="json")
   def my_function():
       # Function code...

Technical details:

* Uses WAL journaling mode for better concurrency and reliability
* File-based locking via ``portalocker`` for thread safety
* Supports reentrant locks

Redis Backend
------------

The Redis backend stores state in a Redis database. It's best suited for:

* Distributed applications
* Multi-process environments
* Web applications and microservices
* Scenarios requiring high throughput

Configuration options:

* ``redis_url``: Redis connection URL (default: ``"redis://localhost:6379/0"``)
* ``serializer``: Serialization format (``"pickle"`` or ``"json"``)
* ``prefix``: Key prefix in Redis (default: ``"statefulpy:"``)
* ``lock_timeout``: Lock timeout in milliseconds (default: ``30000``)

Example:

.. code-block:: python

   @stateful(
       backend="redis", 
       redis_url="redis://user:password@hostname:6379/0",
       serializer="json"
   )
   def my_function():
       # Function code...

Technical details:

* Uses Redis atomic operations for distributed locking (``SET NX PX``)
* Supports reentrant locks across processes
* Keys are prefixed to avoid collisions with other applications

Custom Backends
--------------

StatefulPy allows registering custom backends:

.. code-block:: python

   from statefulpy.backends.base import StateBackend, register_backend

   class MyCustomBackend(StateBackend):
       # Implement required methods...
       
   register_backend("custom", "path.to.module:MyCustomBackend")
