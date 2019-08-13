DBus Starter Address
====================

Print environment variables when D-Bus' service activation feature is used.

D-Bus offers a "service activation" feature. This feature lets peers be lazily
started. More specifically, if all of the following are true:

1.  A message is sent to a name (e.g. ``org.example.MyService1``).
2.  No peer has claimed that name.
3.  A D-Bus service file has been installed for that name.

…then the message bus will buffer the message, start a process, wait for it to
connect to the bus and claim the relevant name, and then deliver the message.

After a process has been started by the message bus, it should connect to the
bus at ``DBUS_STARTER_ADDRESS`` and consume the buffered messages:

    The executable launched will have the environment variable
    ``DBUS_STARTER_ADDRESS`` set to the address of the message bus so it can
    connect and request the appropriate names.

    The executable being launched may want to know whether the message bus
    starting it is one of the well-known message buses (see the section called
    “Well-known Message Bus Instances”). To facilitate this, the bus must also
    set the ``DBUS_STARTER_BUS_TYPE`` environment variable if it is one of the
    well-known buses. The currently-defined values for this variable are system
    for the systemwide message bus, and session for the per-login-session
    message bus. The new executable must still connect to the address given in
    ``DBUS_STARTER_ADDRESS``, but may assume that the resulting connection is to
    the well-known bus.

    -- `D-Bus Specification`_

Unfortunately, the ``DBUS_STARTER_*`` environment variables are only set if the
message bus directly starts the process. If the message bus delegates this task
to systemd, neither environment variable is set. This is unfortunate, because
systemd is better equipped to manage services.

This directory contains a minimal set of files designed to reproduce this
behaviour. To use, start by installing a D-Bus service and monitoring its
output:

.. code-block:: sh

    scripts/install.sh  # into home directory
    journalctl --user --follow

Then, trigger service activation by sending a D-Bus message:

.. code-block:: sh

    dbus-send \
        --dest=name.jerebear.MyService1 \
        /com/example/Foo1 \
        com.example.Foo1.Method

When you're done, you can uninstall the installed files:

.. code-block:: sh

    scripts/uninstall.sh

.. NOTE::
    The D-Bus service is badly behaved behaved. It does not connect to the
    activating D-Bus bus and consume buffered messages. The message buffer may
    grow infinitely.

.. _D-Bus Specification: https://dbus.freedesktop.org/doc/dbus-specification.html
