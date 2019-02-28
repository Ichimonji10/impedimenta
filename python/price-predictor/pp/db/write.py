# coding=utf-8
"""Functions for inserting rows into the database.

Some of the functions in this modules use UPSERT-style statements. SQLite added
support for `UPSERT`_ in version 3.24.0, which was released on 2018-06-24.

.. _UPSERT: https://www.sqlite.org/lang_UPSERT.html
"""
import json
from typing import Iterable, Sequence, Union

from pp.constants import (
    MEANS_TABLE,
    MODELS_TABLE,
    STD_DATA_TABLES,
    STD_DEVS_TABLE,
)
from pp.db import common, read


def means(rows: Iterable[common.MeansRow]) -> None:
    """Insert rows into the :data:`pp.constants.MEANS_TABLE`.

    :param rows: The rows to insert.
    """
    statement = (
        f"""
        INSERT INTO {MEANS_TABLE} VALUES (
            :table_name,
            :column_name,
            :mean)
        ON CONFLICT (table_name, column_name) DO UPDATE SET
            mean=:mean
        """
    )
    values = (
        {
            'table_name': row.table_name,
            'column_name': row.column_name,
            'mean': row.mean,
        }
        for row in rows
    )
    with common.get_db_conn() as conn:
        with conn:
            conn.executemany(statement, values)


def std_devs(rows: Iterable[common.StdDevsRow]) -> None:
    """Insert rows into the :data:`pp.constants.STD_DEVS_TABLE`.

    :param rows: The rows to insert.
    """
    statement = (
        f"""
        INSERT INTO {STD_DEVS_TABLE} VALUES (
            :table_name,
            :column_name,
            :std_dev)
        ON CONFLICT (table_name, column_name) DO UPDATE SET
            std_dev=:std_dev
        """
    )
    values = (
        {
            'table_name': row.table_name,
            'column_name': row.column_name,
            'std_dev': row.std_dev,
        }
        for row in rows
    )
    with common.get_db_conn() as conn:
        with conn:
            conn.executemany(statement, values)


def std_scores(
        table_name: str,
        rows: Iterable[Sequence[Union[float, str]]]) -> None:
    """Insert rows into one of the :data:`pp.constants.STD_DATA_TABLES`.

    :param table_name: The target table.
    :param rows: The rows to insert.
    """
    if table_name not in STD_DATA_TABLES:
        raise ValueError(
            f'Table "{table_name}" is not one of {STD_DATA_TABLES}'
        )
    qmarks: str = ', '.join('?' for _ in read.meta_column_names())
    with common.get_db_conn() as conn:
        with conn:
            conn.executemany(f'INSERT INTO {table_name} VALUES ({qmarks})', rows)


def models(rows: Iterable[common.ModelsRow]) -> None:
    """Insert rows into the :data:`pp.constants.MODELS_TABLE`.

    :param rows: The rows to insert.
    """
    statement = (
        f"""
        INSERT INTO {MODELS_TABLE} values (
            :output_column,
            :cost,
            :offset,
            :input_columns)
        ON CONFLICT (output_column) DO UPDATE SET
            cost=:cost,
            offset=:offset,
            input_columns=:input_columns
        """
    )
    values = (
        {
            'output_column': row.output_column,
            'cost': row.cost,
            'offset': row.offset,
            'input_columns': json.dumps(row.input_columns),
        }
        for row in rows
    )
    with common.get_db_conn() as conn:
        with conn:
            conn.executemany(statement, values)
