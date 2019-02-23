# coding=utf-8
"""Utilities for working with D-Bus."""
import signal
from collections import namedtuple
from typing import Iterable

import gi
gi.require_version('Gtk', '3.0')  # pylint:disable=wrong-import-position
from gi.repository import GLib, Gio

Event = namedtuple('Event', ('none', 'new', 'removed'))

EVENT = Event(' ', '+', '-')

Unit = namedtuple('Unit', (
    'name',
    'description',
    'load_state',
    'active_state',
    'sub_state',
    'following',
    'object_path',
    'queued_job',
    'job_type',
    'job_path',
))

UnitNew = namedtuple('UnitNew', ('id', 'unit'))

UnitRemoved = namedtuple('UnitRemoved', ('id', 'unit'))


# Ignore too-few-methods because this is a small toy application, and it
# doesn't need to be fully fleshed out.
class Main:  # pylint:disable=too-few-public-methods
    """Monitor unit appearances and disappearances."""

    def __init__(self):
        """Subscribe to signals, catch SIGINT, and run the GLib main loop."""
        connection: Gio.DBusConnection = Gio.bus_get_sync(
            bus_type=Gio.BusType.SYSTEM,
            cancellable=None,
        )

        # NOTE: If the goal of this application is to actually *track* extant
        # units, then this should be executed after the signals below are
        # enabled. Simply moving this block of code down won't do the trick, as
        # signals are processed by main loops. It might be fruitful to
        # investigate creating multiple main loops within multiple threads.
        for unit in get_units(connection):
            print_unit_name(unit.name, EVENT.none)

        connection.signal_subscribe(
            sender='org.freedesktop.systemd1',
            interface_name='org.freedesktop.systemd1.Manager',
            member='UnitRemoved',
            object_path='/org/freedesktop/systemd1',
            arg0=None,
            flags=Gio.DBusSignalFlags.NONE,
            callback=handle_unit_removed,
            user_data=None,
        )
        connection.signal_subscribe(
            sender='org.freedesktop.systemd1',
            interface_name='org.freedesktop.systemd1.Manager',
            member='UnitNew',
            object_path='/org/freedesktop/systemd1',
            arg0=None,
            flags=Gio.DBusSignalFlags.NONE,
            callback=handle_unit_new,
            user_data=None,
        )
        self.main_loop = GLib.MainLoop()
        signal.signal(signal.SIGINT, self.handle_sigint)
        self.main_loop.run()

    def handle_sigint(self, signum, frame):  # pylint:disable=unused-argument
        """Quit the GLib main loop.

        SIGINT is emitted when a user presses ctrl+c.
        """
        self.main_loop.quit()


def get_units(connection: Gio.DBusConnection) -> Iterable[Unit]:
    """Get all extant units."""
    response = connection.call_sync(
        bus_name='org.freedesktop.systemd1',
        object_path='/org/freedesktop/systemd1',
        interface_name='org.freedesktop.systemd1.Manager',
        method_name='ListUnits',
        parameters=None,
        reply_type=GLib.VariantType.new('(a(ssssssouso))'),
        flags=Gio.DBusCallFlags.NONE,
        timeout_msec=-1,
        cancellable=None,
    )
    return tuple(Unit(*unit_props) for unit_props in response.unpack()[0])


# Ignore argument issues because the PyGObject API defines what's available.
def handle_unit_new(  # pylint:disable=too-many-arguments,unused-argument
        connection,
        sender_name,
        object_path,
        interface_name,
        signal_name,
        parameters,
        *user_data) -> None:
    """Handle the ``UnitNew`` signal."""
    unit_new = UnitNew(*parameters.unpack())
    print_unit_name(unit_new.id, EVENT.new)


# Ignore argument issues because the PyGObject API defines what's available.
def handle_unit_removed(  # pylint:disable=too-many-arguments,unused-argument
        connection,
        sender_name,
        object_path,
        interface_name,
        signal_name,
        parameters,
        *user_data) -> None:
    """Handle the ``UnitRemoved`` signal."""
    unit_removed = UnitRemoved(*parameters.unpack())
    print_unit_name(unit_removed.id, EVENT.removed)


def print_unit_name(unit_name: str, prefix: str = EVENT.none) -> None:
    """Print the given unit's name to stdout."""
    print(prefix, unit_name)


if __name__ == '__main__':
    Main()
