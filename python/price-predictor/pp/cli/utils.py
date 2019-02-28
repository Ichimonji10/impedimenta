# coding=utf-8
"""Utilities for the CLI interfaces."""
import argparse
import sys
from multiprocessing import connection, cpu_count
from typing import Optional, Union


def add_jobs_flag(parser: argparse.ArgumentParser) -> None:
    """Add the ``--jobs`` flag to a parser."""
    default = cpu_count()
    parser.add_argument(
        '-j',
        '--jobs',
        default=default,
        help=f'Spawn this many processes, instead of {default}.',
        type=int,
    )

def add_overwrite_flags(
        parser: argparse.ArgumentParser,
        helptext: str) -> None:
    """Add the ``--{no-,}overwrite`` flags to a parser."""
    # See: https://stackoverflow.com/a/15008806
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--overwrite',
        action='store_true',
        dest='overwrite',
        help=helptext,
    )
    group.add_argument(
        '--no-overwrite',
        action='store_false',
        dest='overwrite',
        help='Inverse of --overwrite',
    )
    group.set_defaults(overwrite=False)


def add_progress_flags(parser: argparse.ArgumentParser) -> None:
    """Add the ``--{no-,}progress`` flags to a parser."""
    # See: https://stackoverflow.com/a/15008806
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--progress',
        action='store_true',
        dest='progress',
        help='Show progress messages.',
    )
    group.add_argument(
        '--no-progress',
        action='store_false',
        dest='progress',
        help="Don't show progress messages.",
    )
    group.set_defaults(progress=False)


def report_progress(
        conn_out: connection.Connection,
        denominator: int,
        prefix: Optional[str] = None) -> None:
    """Tell the user how much work has been done.

    :param conn_out: A multiprocessing ``Connection`` object from which values
        may be read. Each value emitted by the object should be an integer.
        Progress is calculated with ``numerator / denominator``.

        This function will exit when ``None`` is read.
    :param denominator: Used to calculate progress.
    :param prefix: A message to print before the progress prompt, e.g.
        'Progress: '.
    :raise: ``ValueError`` if ``denominator`` is zero.
    :return: Nothing.
    """
    if denominator == 0:
        raise ValueError('Denominator must not be zero.')
    if prefix is None:
        prefix = ''
    while True:
        numerator: Union[int, None] = conn_out.recv()
        if numerator is None:
            conn_out.close()
            print()
            break
        percent: float = (numerator / denominator) * 100
        # \r is carriage return. The other is an ANSI escape code. See:
        # https://en.wikipedia.org/wiki/ANSI_escape_code
        print(f'\r\033[K{prefix}{percent:.0f}%', end='')
        sys.stdout.flush()
