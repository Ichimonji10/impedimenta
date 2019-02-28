# coding=utf-8
"""Utilities for the top-level modules."""
import itertools
import weakref
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import Callable, Iterator, Optional, Sequence

from pp.constants import DATA_TABLES, STD_DATA_TABLES


def get_data_table(std_table_name: str) -> str:
    """Get the data table corresponding to the given standard data table."""
    idx = STD_DATA_TABLES.index(std_table_name)
    return DATA_TABLES[idx]


def varying_combinations(
        iterable: Sequence[str]) -> Iterator[Sequence[str]]:
    """Yield all combinations of ``iterable`` of at least length 1.

    For example:

    >>> columns = ('c', 'a')
    >>> gen = varying_combinations(columns)
    >>> next(gen)
    ('c', 'a')
    >>> next(gen)
    ('c',)
    >>> next(gen)
    ('a',)
    >>> try:
    ...     next(gen)
    ... except StopIteration:
    ...     pass

    :param iterable: The iterable from which to form combinations.
    :return: An iterator that returns combinations from ``iterable``.
    """
    # Yield longest combinations first to help ensure that any multiprocessing
    # pool making use of this function can keep all workers busy.
    #
    # tuple(range(4))        → (0, 1, 2, 3)
    # tuple(range(4, 0, -1)) → (4, 3, 2, 1)
    for i in range(len(iterable), 0, -1):
        yield from itertools.combinations(iterable, i)


# This class is the right size.
class PressSecretary:  # pylint:disable=too-few-public-methods
    """Send missives to a reporter.

    When this class is instantiated, it creates a reporter process.
    Asynchronous updates may be sent to it with the :meth:`update` method. When
    this class is garbage collected, the reporter process is synchronously
    killed. This class is designed to work hand-in-hand with
    :func:`pp.cli.utils.report_progress`.
    """

    def __init__(
            self,
            reporter: Callable,
            denominator: int,
            prefix: Optional[str] = None) -> None:
        """Create a reporter process."""
        conn_out: Connection
        self.conn_in: Connection
        conn_out, self.conn_in = Pipe(duplex=False)
        reporter_proc = Process(
            target=reporter,
            args=(conn_out, denominator, prefix)
        )
        reporter_proc.start()

        # Do **NOT** give func, args, or kwargs any references to self. This
        # implies avoiding bound (instance) methods, among other things. See:
        # https://docs.python.org/3/library/weakref.html#weakref.finalize
        weakref.finalize(
            self,
            self.__cleanup,
            self.conn_in,
            reporter_proc,
        )

    def update(self, numerator: int) -> None:
        """Send an update to the reporter process."""
        self.conn_in.send(numerator)

    @staticmethod
    def __cleanup(conn_in: Connection, reporter: Process) -> None:
        """Synchronously kill the reporter process."""
        conn_in.send(None)
        reporter.join()
