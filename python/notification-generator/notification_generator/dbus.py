# coding=utf-8
"""Utilities for working with dbus."""
import gi
gi.require_version('Gtk', '3.0')  # pylint:disable=wrong-import-position
from gi.repository import GLib, Gio


def send(summary: str, body: str) -> None:
    """Send a message to the notification service.

    :param summary: The summary text briefly describing the notification.
    :param body: The detailed body text.
    """
    parameters = GLib.Variant('(susssasa{sv}i)', (
        'Notification Generator',
        0,  # unsigned int
        '',
        summary,
        body,
        [],  # List[str]
        {},
        -1,
    ))
    proxy = Gio.DBusProxy.new_for_bus_sync(
        bus_type=Gio.BusType.SESSION,
        flags=Gio.DBusProxyFlags.NONE,
        info=None,
        name='org.freedesktop.Notifications',
        object_path='/org/freedesktop/Notifications',
        interface_name='org.freedesktop.Notifications',
        cancellable=None,
    )
    proxy.call_sync(
        method_name='Notify',
        parameters=parameters,
        flags=Gio.DBusCallFlags.NONE,
        timeout_msec=-1,  # use default timeout
        cancellable=None,
    )
