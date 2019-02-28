# coding=utf-8
"""Tools used by the other database management modules."""
import contextlib
import csv
import importlib
import sqlite3
from pathlib import Path
from typing import (
    Any,
    Callable,
    IO,
    Iterator,
    Mapping,
    NamedTuple,
    Optional,
    Sequence,
)

from xdg import BaseDirectory

from pp import exceptions
from pp.constants import DB_FILE


class MeansRow(NamedTuple):
    """A row from the :data:`pp.constants.MEANS_TABLE`."""
    table_name: str
    column_name: str
    mean: float


class StdDevsRow(NamedTuple):
    """A row from the :data:`pp.constants.STD_DEVS_TABLE`."""
    table_name: str
    column_name: str
    std_dev: float


class ModelsRow(NamedTuple):
    """A row from the :data:`pp.constants.MODELS_TABLE`.

    A least-squares linear matrix equation that predicts an output (dependent)
    column given some number of input (independent) columns. A model's cost is
    a single numeric value which sums the error and complexity of a model,
    where a high error or a high complexity are both bad.

    For example, given the following equation::

        bathrooms = 0.5 * floors + 1

    A model would be constructed as follows::

        ModelsRow(
            output_column='bathrooms',
            cost=0.6,  # model under-fits reality, has high cost
            offset=1,
            input_columns={'floors': 0.5},
        )
    """
    output_column: str
    cost: float
    offset: float
    input_columns: Mapping[str, float]


@contextlib.contextmanager
def get_db_conn(db_path: Optional[Path] = None) -> Iterator[sqlite3.Connection]:
    """Return a context manager which yields a database connection.

    :param db_path: The path to a SQLite 3 database.
    :return: A sqlite3 `Connection`_ object. It will automatically be closed
        when this context manager exits.

    .. _Connection:
        https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
    """
    if not db_path:
        db_path = get_load_path()
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def get_load_path() -> Path:
    """Return the path to the database file.

    :return: The path to the database.
    :raise pp.exceptions.DatabaseNotFoundError: If the database isn't found.
    """
    importlib.reload(BaseDirectory)
    for db_dir in BaseDirectory.load_data_paths(DB_FILE.parent):
        db_path = Path(db_dir, DB_FILE.name)
        if db_path.exists():
            return db_path
    raise exceptions.DatabaseNotFoundError(
        'Unable to find a database. A database should be present at one of '
        'the following paths: ' + ', '.join((
            str(db_dir)
            for db_dir in BaseDirectory.load_data_paths(DB_FILE.parent)
        ))
    )


def get_save_path() -> Path:
    """Return a path to where a database file may be created.

    Create intermediate directories as needed.
    """
    importlib.reload(BaseDirectory)
    return Path(
        BaseDirectory.save_data_path(DB_FILE.parent),
        DB_FILE.name,
    )


def parse_csv(
        handle: IO[str],
        caster: Callable[[Sequence[str]], Sequence[Any]] = lambda row: row,
        header_rows: int = 1):
    """Read a CSV file and yield a parsed tuple per consumed row.

    :param handle: The handle to an input stream.
    :param caster: A callable which accepts a sequence of strings, and returns
        a new sequence of the same length. The new sequence doesn't have to be
        of the same type. For example:

        .. code-block:: python

            def caster(fields):
                return (int(fields[0]), float(fields[1]))

        The default returns input as-is.
    :param header_rows: The number of header rows in the input file. Header
        rows are ignored.
    :return: A generator yielding sequences, where each sequence of is a row
        from the input file.
    """
    for i, row in enumerate(csv.reader(handle)):
        if i < header_rows:
            continue
        yield caster(row)
