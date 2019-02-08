# coding=utf-8
"""Utilities for working with dbus."""
from jeepney import DBusAddress, new_method_call
from jeepney.integrate.blocking import connect_and_authenticate


def send(summary: str, body: str) -> None:
    """Send a message to the notification service.

    :param summary: The summary text briefly describing the notification.
    :param body: The detailed body text.
    """
    notifications_app = DBusAddress(
        '/org/freedesktop/Notifications',
        bus_name='org.freedesktop.Notifications',
        interface='org.freedesktop.Notifications',
    )
    msg = new_method_call(
        remote_obj=notifications_app,
        method='Notify',
        signature='susssasa{sv}i',
        body=(
            'Notification Generator',
            0,
            '',
            summary,
            body,
            [],
            {},
            -1,
        ),
    )
    connection = connect_and_authenticate(bus='SESSION')
    connection.send_and_get_reply(msg)
