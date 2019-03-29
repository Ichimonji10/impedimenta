# coding=utf-8
"""Functions for reading the database."""
import json
from typing import Any, Iterator, List, Optional, Sequence

from pp import exceptions
from pp.constants import (
    CATEGORICAL_TYPE,
    CONTINUOUS_TYPE,
    DATA_FILE,
    MEANS_TABLE,
    METADATA_FILE,
    MODELS_TABLE,
    STD_DEVS_TABLE,
    STD_TRAINING_TABLE,
)
from pp.db import common


def column_names(table_name: str) -> Iterator[str]:
    """Get the name of every column in the given table.

    .. NOTE:: Column names are yielded in the same order as they are defined on
        the target table.

    :param table: The table to inspect.
    :raise: ``ValueError`` if the given table name doesn't exist.
    :return: An iterator that returns column names.
    """
    table_names_ = table_names()
    if table_name not in table_names_:
        raise ValueError(
            f'The table {table_name} does not exist. Tables are '
            ", ".join(table_names_)
        )
    with common.get_db_conn() as conn:
        row: Sequence[str]
        for row in conn.execute(
                'SELECT name FROM pragma_table_info(?)',
                (table_name,)):
            yield row[0]


def meta_column_names(column_type_: Optional[str] = None) -> Iterator[str]:
    """Get the ``column_names`` column from the ``meta`` table.

    .. NOTE:: Column names are not yielded in a specific order.

    :param column_type_: Filter the yielded column names. Only return column
        names that are of the given type. One of
        :data:`pp.constants.COLUMN_TYPES`.
    :return: An iterator that returns column names.
    """
    statement: str = 'SELECT column_name FROM meta'
    args: List[str] = []
    if column_type_:
        statement += ' WHERE column_type == ?'
        args.append(column_type_)

    with common.get_db_conn() as conn:
        row: Sequence[str]
        for row in conn.execute(statement, args):
            yield row[0]


def mean(table_name: str, column_name: str) -> float:
    """Get a value from the :data:`pp.constants.MEANS_TABLE`.

    :param table_name: The table for which a mean is being fetched. One of
        :data:`pp.constants.DATA_TABLES`.
    :param column_name: The column for which a mean is being fetched.
    :return: The mean of the given column in the given table.
    :raise pp.exceptions.MissingValueError: If no mean has been calculated for
        the given column in the given table.
    """
    rows: Sequence[common.MeansRow] = tuple(means(table_name, column_name))
    try:
        return rows[0].mean
    except IndexError:
        raise exceptions.MissingValueError(
            f'No mean has been calculated for table "{table_name}", column '
            f'"{column_name}".'
        )


def means(
        table_name: Optional[str] = None,
        column_name: Optional[str] = None) -> Iterator[common.MeansRow]:
    """Get rows from the :data:`pp.constants.MEANS_TABLE`.

    :param table_name: Narrow results by only returning cached means for this
        table.
    :param column_name: Narrow results by only returning the cached mean for
        this column.
    :return: An iterator that returns rows.
    """
    statement: str = f'SELECT * FROM {MEANS_TABLE}'
    args: List[str] = []
    if table_name:
        statement += ' WHERE table_name = ?'
        args.append(table_name)
    if column_name:
        statement += ' AND column_name = ?'
        args.append(column_name)

    with common.get_db_conn() as conn:
        for row in conn.execute(statement, args):
            yield common.MeansRow(*row)


def table(
        table_name: str,
        column_names_: Optional[Sequence[str]] = None,
        ) -> Iterator[Sequence[Any]]:
    """Read rows from a table.

    :param table_name: The table to read.
    :param column_names: Return only these columns, instead of all columns.
    :return: An iterator that returns rows.
    """
    if table_name not in table_names():
        raise ValueError(
            f'{table_name} is not a valid table. Tables are: '
            ", ".join(table_names())
        )

    sql_column_names: str
    if column_names_ is None:
        sql_column_names = '*'
    else:
        target_column_names = set(column_names_)
        actual_column_names = set(column_names(table_name))
        if not target_column_names.issubset(actual_column_names):
            raise ValueError(
                'The following columns do not exist: '
                f'{target_column_names - actual_column_names}'
            )
        sql_column_names = ', '.join(
            f'"{column_name}"' for column_name in column_names_
        )

    with common.get_db_conn() as conn:
        for row in conn.execute(f'SELECT {sql_column_names} FROM {table_name}'):
            yield row


def std_dev(table_name: str, column_name: str) -> float:
    """Get a value from the :data:`pp.constants.STD_DEVS_TABLE`.

    :param table_name: The table for which a standard deviation is being
        fetched. One of :data:`pp.constants.DATA_TABLES`.
    :param column_name: The column for which standard deviation is being
        fetched.
    :return: The standard deviation of the given column in the given table.
    :raise pp.exceptions.MissingValueError: If no standard deviation has been
        calculated for the given column in the given table.
    """
    rows: Sequence[common.StdDevsRow] = tuple(
        std_devs(table_name, column_name)
    )
    try:
        return rows[0].std_dev
    except IndexError:
        raise exceptions.MissingValueError(
            f'No standard deviation has been calculated for table '
            f'"{table_name}", column "{column_name}".'
        )


def std_devs(
        table_name: Optional[str] = None,
        column_name: Optional[str] = None) -> Iterator[common.StdDevsRow]:
    """Get rows from the :data:`pp.constants.STD_DEVS_TABLE`.

    :param table_name: Narrow results by only returning cached standard
        deviations for this table.
    :param column_name: Narrow results by only returning the cached standard
        deviation for this column.
    :return: An iterator that returns rows.
    """
    statement: str = f'SELECT * FROM {STD_DEVS_TABLE}'
    args: List[str] = []
    if table_name:
        statement += ' WHERE table_name = ?'
        args.append(table_name)
    if column_name:
        statement += ' AND column_name = ?'
        args.append(column_name)

    with common.get_db_conn() as conn:
        for row in conn.execute(statement, args):
            yield common.StdDevsRow(*row)


def table_names() -> Iterator[str]:
    """Get the name of every table.

    :return: An iterator that returns table names.
    """
    with common.get_db_conn() as conn:
        for row in conn.execute(
                'SELECT name FROM sqlite_master WHERE type = "table"'):
            yield row[0]


def column_type(column_name: str) -> str:
    """Get the type of a column from the "meta" table.

    :param column_name: A column in one of the
        :data:`pp.constants.DATA_TABLES`.
    :return: Either :data:`pp.constants.CATEGORICAL_TYPE` or
        :data:`pp.constants.CONTINUOUS_TYPE`.
    :raise pp.exceptions.MissingValueError: If no type is defined for the given
        column.
    """
    with common.get_db_conn() as conn:
        row: Sequence[str] = conn.execute(
            'SELECT column_type FROM meta WHERE column_name = ?',
            (column_name,)
        ).fetchone()
    if row is None:
        raise exceptions.MissingValueError(
            f'No type is defined for column "{column_name}". Is there a name '
            f'mismatch between {DATA_FILE} and {METADATA_FILE}, or is '
            f'{METADATA_FILE} missing a row?'
        )
    assert row[0] in (CATEGORICAL_TYPE, CONTINUOUS_TYPE)
    return row[0]


def model(output_column: str) -> common.ModelsRow:
    """Get a model for the given ``output_column``.

    Get the row from the :data:`pp.constants.MODELS_TABLE` for the given
    ``output_column``.
    """
    statement = f'SELECT * FROM {MODELS_TABLE} WHERE output_column = ?'
    values = (output_column,)
    with common.get_db_conn() as conn:
        row: Optional[Sequence] = conn.execute(statement, values).fetchone()
    if row is None:
        raise exceptions.PredictionError(
            f"Can't predict {output_column}, as no model for that column has "
            'yet been generated.'
        )
    assert row[0] == output_column
    cost = row[1]
    offset = row[2]
    input_columns = json.loads(row[3])
    return common.ModelsRow(output_column, cost, offset, input_columns)


def zip_codes() -> Iterator[str]:
    """Select zip codes from the :data:`pp.constants.STD_TRAINING_TABLE`."""
    statement = f'SELECT DISTINCT(zipcode) FROM {STD_TRAINING_TABLE}'
    with common.get_db_conn() as conn:
        for row in conn.execute(statement):
            yield row[0]


def zip_code_price(zip_code: str) -> Iterator:
    """Select the given zip code and price from the std training table."""
    statement = f"""
        SELECT zipcode, price FROM {STD_TRAINING_TABLE}
        WHERE zipcode = ?
    """
    values = (zip_code,)
    with common.get_db_conn() as conn:
        for row in conn.execute(statement, values):
            yield row
