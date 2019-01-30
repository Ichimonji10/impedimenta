#!/usr/bin/env python3
# coding=utf-8
"""Send a message to the desktop."""
__version__ = '0.1'

from jeepney import DBusAddress, new_method_call
from jeepney.integrate.blocking import connect_and_authenticate


def main():
    """Send a message to the desktop."""
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
            'dbus-01',
            0,
            '',
            'summary text',
            'body text',
            [],
            {},
            -1,
        ),
    )
    connection = connect_and_authenticate(bus='SESSION')
    reply = connection.send_and_get_reply(msg)
    print(reply)


if __name__ == '__main__':
    main()
