# coding=utf-8
"""Functions for counting rows in the database."""
from typing import Sequence

from pp.db import common, read


def rows(table_name: str) -> int:
    """Count the number of rows in a table.

    :param table_name: The target table.
    """
    table_names = read.table_names()
    assert table_name in table_names
    with common.get_db_conn() as conn:
        row: Sequence[int] = conn.execute(
            f'SELECT COUNT(*) FROM {table_name}'
        ).fetchone()
    return row[0]
