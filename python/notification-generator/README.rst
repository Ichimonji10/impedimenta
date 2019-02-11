Notification Generator
======================

This application generates a desktop notification with D-Bus. A good way to make
use of this program is to do the following:

1. Read portions of the `D-Bus Specification`_.
2. Read portions of the `Desktop Notification Specification`_.
3. Read and execute this code.

Doing this should allow one to learn some basic D-Bus concepts.

To install, clone the source code, ``cd`` into its directory, and execute the
following:

.. code-block:: sh

    python3 -m venv ~/.venvs/dbus-01
    source ~/.venvs/dbus-01/bin/activate
    pip install --upgrade pip
    pip install .

You can now call the ``ng-*`` CLI utilities. If PyGObject installation fails,
try running through the instructions for `creating a development environment`_.

.. _creating a development environment: https://pygobject.readthedocs.io/en/latest/devguide/dev_environ.html
.. _d-bus specification:  https://dbus.freedesktop.org/doc/dbus-specification.html
.. _desktop notification specification: https://developer.gnome.org/notification-spec/
