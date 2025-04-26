Quickstart Guide
===============

Installation
-----------

Install StatefulPy using pip:

.. code-block:: bash

   pip install statefulpy

For Redis support:

.. code-block:: bash

   pip install statefulpy[redis]

Basic Usage
----------

Here's a simple counter example:

.. code-block:: python

   from statefulpy import stateful

   @stateful
   def counter():
       if "count" not in counter.state:
           counter.state["count"] = 0
       counter.state["count"] += 1
       return counter.state["count"]

   # Call the function
   print(counter())  # 1
   print(counter())  # 2

   # Even if you restart your program, the count will continue
   # from where it left off!

Backends
--------

SQLite Backend (Default)
~~~~~~~~~~~~~~~~~~~~~~~

For single-process applications or local development:

.. code-block:: python

   @stateful(backend="sqlite", db_path="state.db")
   def my_function():
       # Your function code...

Redis Backend
~~~~~~~~~~~

For distributed applications or multi-process environments:

.. code-block:: python

   @stateful(backend="redis", redis_url="redis://localhost:6379/0")
   def my_function():
       # Your function code...

Serialization
------------

StatefulPy supports multiple serialization formats:

.. code-block:: python

   # Using JSON serializer for human-readable storage
   @stateful(backend="sqlite", db_path="state.db", serializer="json")
   def my_function():
       # Your function code...

   # Using the default pickle serializer for better performance
   @stateful(backend="sqlite", db_path="state.db", serializer="pickle")
   def my_function():
       # Your function code...
