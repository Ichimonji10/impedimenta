intersphinx-path-root
=====================

This package doesn't provide any Python namespaces. Instead, it serves to knit
together the documentation for several other Python packages all into a
cohesive whole. To build documentation:

.. code-block:: bash

    ./compile.sh
    ./serve.sh

You can then visit http://localhost:8080.

The compilation process is done locally, and it assumes that Python 3 and
`poetry`_ are available. It might be possible to make the build process more
system-independent by Dockerizing the build process too.

.. _poetry: https://python-poetry.org/
