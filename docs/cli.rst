Command-Line Interface
=====================

StatefulPy includes a command-line interface (CLI) for managing backends and state data.

Basic Usage
----------

.. code-block:: bash

   statefulpy [command] [options]

Available Commands
----------------

Initialize a Backend
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   statefulpy init --backend sqlite --path data/app_state.db
   statefulpy init --backend redis --path redis://localhost:6379/0

This command initializes a backend for use with StatefulPy. It creates any necessary
database structures and verifies connectivity.

Migrate Between Backends
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   statefulpy migrate --from sqlite --to redis \
     --from-path data/app_state.db \
     --to-path redis://localhost:6379/0

This command migrates state data from one backend to another. This is useful when
you want to move from SQLite to Redis for scaling up.

Health Check
~~~~~~~~~~~

.. code-block:: bash

   statefulpy healthcheck --backend sqlite --path data/app_state.db

This command checks if a backend is functioning properly. It verifies that the
backend can be connected to and that state operations work.

List Functions
~~~~~~~~~~~~~

.. code-block:: bash

   statefulpy list --backend sqlite --path data/app_state.db

This command lists all stateful functions stored in a backend.

Common Options
-----------

* ``--backend``: Specify the backend type (``sqlite`` or ``redis``)
* ``--path``: Path to the database file (SQLite) or Redis URL

Troubleshooting
-------------

* Ensure all paths are absolute or relative to your current directory
* Verify Redis is running if using the Redis backend
* Check permissions on SQLite database files
* Use the healthcheck command to verify backend connectivity
