# coding=utf-8
"""Utilities for working with dbus."""
from PyQt5.QtCore import QMetaType, QVariant
from PyQt5.QtDBus import QDBusArgument, QDBusInterface


def send(summary: str, body: str) -> None:
    """Send a message to the notification service.

    :param summary: The summary text briefly describing the notification.
    :param body: The detailed body text.
    """
    interface = QDBusInterface(
        'org.freedesktop.Notifications',
        '/org/freedesktop/Notifications',
        'org.freedesktop.Notifications',
    )
    response = interface.call(
        'Notify',
        'Notification Generator',
        get_replaces_id(),
        '',
        summary,
        body,
        get_actions(),
        {},
        -1,
    )
    print(response.errorName())
    print(response.errorMessage())


def get_actions():
    return QDBusArgument([], QMetaType.QStringList)


def get_replaces_id():
    replaces_id = QVariant(0)
    replaces_id.convert(QVariant.UInt)
    return replaces_id
