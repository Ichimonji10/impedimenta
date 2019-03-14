#!/usr/bin/env python3
# coding=utf-8
#
# It's fine for a class to have a focused definition.
# pylint:disable=too-few-public-methods
"""Encapsulate reporter management in a class."""
import sys
import time
import weakref
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import Callable, Union


def main():
    """Execute business logic."""
    denominator = 5
    press_secretary = PressSecretary(report_progress, denominator)
    for numerator in range(denominator + 1):
        press_secretary.update(numerator)
        time.sleep(0.5)
    del press_secretary
    print('The press secretary has been deleted.')


class PressSecretary:
    """Send missives to a reporter."""

    def __init__(self, reporter: Callable, denominator: int):
        """Create a reporter process."""
        conn_out: Connection
        self.conn_in: Connection
        conn_out, self.conn_in = Pipe(duplex=False)
        reporter_proc = Process(target=reporter, args=(conn_out, denominator))
        reporter_proc.start()

        # Do **NOT** schedule a call to a bound (instance) method. See:
        # https://docs.python.org/3/library/weakref.html#weakref.finalize
        weakref.finalize(
            self,
            self.__cleanup,
            self.conn_in,
            reporter_proc,
        )

    def update(self, numerator):
        """Send an update to the reporter process."""
        self.conn_in.send(numerator)

    @staticmethod
    def __cleanup(conn_in: Connection, reporter: Process):
        """Synchronously kill the reporter process."""
        conn_in.send(None)
        reporter.join()
        print('The press secretary has deleted the reporter.')


def report_progress(
        conn_out: Connection,
        denominator: int,
        prefix: str = '') -> None:
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


if __name__ == '__main__':
    main()
