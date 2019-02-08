# coding=utf-8
"""Generate a desktop notification message."""
import argparse

from notification_generator import dbus


def main() -> None:
    """Parse arguments and call business logic."""
    parser = argparse.ArgumentParser(
        description='Generate a desktop notification.',
    )
    parser.add_argument(
        '--summary',
        default='',
        help='The summary text briefly describing the notification.',
        type=str,
    )
    parser.add_argument(
        '--body',
        default='',
        help='The detailed body text.',
        type=str,
    )
    args = parser.parse_args()
    dbus.send(args.summary, args.body)
