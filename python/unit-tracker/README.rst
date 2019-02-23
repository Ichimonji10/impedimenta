Unit Tracker
============

This application tracks which (systemd) units are extant.

To install, clone the source code, ``cd`` into its directory, and execute the
following:

.. code-block:: sh

    python3 -m venv ~/.venvs/dbus-01
    source ~/.venvs/dbus-01/bin/activate
    pip install --upgrade pip
    pip install .

You can now call the ``ut-*`` CLI utilities. If PyGObject installation fails,
try running through the instructions for `creating a development environment`_.

.. _creating a development environment: https://pygobject.readthedocs.io/en/latest/devguide/dev_environ.html
