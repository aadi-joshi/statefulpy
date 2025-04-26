Welcome to StatefulPy's documentation!
======================================

**StatefulPy** provides transparent, persistent state management for regular Python functions.

With StatefulPy, you can easily make any function maintain its state between calls and even
between program restarts, without having to worry about manually saving and loading state.

.. code-block:: python

   from statefulpy import stateful

   @stateful
   def counter():
       if "count" not in counter.state:
           counter.state["count"] = 0
       counter.state["count"] += 1
       return counter.state["count"]

   # The counter value persists across runs
   print(counter())  # 1 (first run)
   print(counter())  # 2
   # Restart your program...
   print(counter())  # 3 (value was loaded from storage)

Contents
--------

.. toctree::
   :maxdepth: 2

   quickstart
   api
   backends
   serializers
   cli
   examples
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
