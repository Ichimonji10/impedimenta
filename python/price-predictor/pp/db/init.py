# coding=utf-8
"""Functions for initializing the database."""
import csv
import random
import re
import sqlite3
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence

from pp import datasets, exceptions
from pp.constants import (
    CATEGORICAL_TYPE,
    COLUMN_TYPES,
    CONTINUOUS_TYPE,
    DATA_FILE,
    DATA_TABLES,
    DATA_TABLE_WEIGHTS,
    MEANS_TABLE,
    METADATA_FILE,
    MODELS_TABLE,
    STD_DATA_TABLES,
    STD_DEVS_TABLE,
)
from pp.db import calc, common, read, write


def cpop_db(dataset_name: str, seed: Optional[int] = None) -> None:
    """Create and populate a database.

    :param dataset: The name of a dataset. A key from
        :func:`pp.datasets.installed`.
    :param seed: Passed to :func:`pp.db.init.populate_tables`.
    :raise DatabaseAlreadyExistsError: If the target database already exists.
    :raise DatasetNotFoundError: If the referenced dataset isn't installed.
    """
    # Check whether a conflicting database exists.
    save_path: Path = common.get_save_path()
    if save_path.exists():
        raise exceptions.DatabaseAlreadyExistsError(
            "Can't create a new database, as a file already exists at: {}"
            .format(save_path),
        )

    # Check whether the dataset to install exists.
    dataset_dirs: Mapping[str, Path] = datasets.installed()
    try:
        dataset_dir: Path = dataset_dirs[dataset_name]
    except KeyError:
        raise exceptions.DatasetNotFoundError(
            f"Can't populate database with dataset {dataset_name}, as it's not "
            'installed'
        )

    # Create and populate a new database.
    with common.get_db_conn(save_path) as conn:
        create_meta_table(conn)
        populate_meta_table(conn, Path(dataset_dir, METADATA_FILE))
        create_data_tables(conn, Path(dataset_dir, DATA_FILE))
        populate_data_tables(conn, Path(dataset_dir, DATA_FILE), seed)
        create_means_table(conn)
        create_std_data_tables(conn)
        create_std_devs_table(conn)
        create_models_table(conn)


def create_meta_table(conn: sqlite3.Connection) -> None:
    """Create and populate the ``meta`` table.

    :param conn: A connection to the target SQLite database.
    """
    with conn:
        conn.execute(
            f"""
            CREATE TABLE meta (
                column_name TEXT NOT NULL PRIMARY KEY,
                column_type TEXT NOT NULL CHECK(
                    column_type == '{CATEGORICAL_TYPE}' OR column_type == '{CONTINUOUS_TYPE}'
                )
            )
            """
        )


def populate_meta_table(conn: sqlite3.Connection, csv_path: Path) -> None:
    """Populate the ``meta`` table.

    :param conn: A connection to the target SQLite database.
    :param csv_path: The path to the CSV file containing metadata about sales.
    """
    with conn:
        with open(csv_path) as handle:
            conn.executemany(
                'INSERT INTO meta VALUES (?, ?)',
                common.parse_csv(handle)
            )


def create_data_tables(conn: sqlite3.Connection, csv_path: Path) -> None:
    """Create the :param:`pp.constants.DATA_TABLES`.

    .. NOTE:: The "meta" table must have been created and populated before
        calling this function. See: :func:`pp.db.init.cpop_meta_table`.

    :param conn: A connection to the target SQLite database.
    :param csv_path: The path to the CSV file containing data about sales.
    :param seed: Rows are assigned to the :data:`pp.constants.DATA_TABLES` in
        approximately the ratio given by
        :data:`pp.constants.DATA_TABLE_WEIGHTS`. The exact row-to-table
        assignments are controlled by a random number generator. If one wishes
        to produce consistent row-to-table assignments, a consistent seed
        should be provided.
    """
    # Are the column names safe looking, and does every column name also appear
    # in the meta table? This is a code smell. See _check().
    with open(csv_path) as handle:
        column_names = next(csv.reader(handle))
    _check(column_names)
    try:
        column_types: Mapping[str, str] = {
            column_name: COLUMN_TYPES[read.column_type(column_name)]
            for column_name in column_names
        }
    except (exceptions.MissingValueError, KeyError) as err:
        raise exceptions.DatabaseCPOPError(
            'The meta CSV file is missing an entry.'
        ) from err

    # Create tables.
    col_defs = ', '.join(
        f"'{column_name}' {column_types[column_name]}"
        for column_name in column_names
    )
    with conn:
        for table in DATA_TABLES:
            conn.execute(f'create table {table} ({col_defs})')


def populate_data_tables(
        conn: sqlite3.Connection,
        csv_path: Path,
        seed: Optional[int]) -> None:
    """Create the :param:`pp.constants.DATA_TABLES`.

    .. NOTE:: The "meta" table must have been created and populated before
        calling this function. See: :func:`pp.db.init.cpop_meta_table`.
    """
    rng = random.Random(seed)
    template = (
        'INSERT INTO {table} VALUES (' +
        ', '.join('?' for _ in read.meta_column_names()) +
        ')'
    )
    with conn:
        with open(csv_path) as handle:
            for row in common.parse_csv(handle):
                table = rng.choices(DATA_TABLES, DATA_TABLE_WEIGHTS)[0]
                statement = template.format(table=table)
                conn.execute(statement, row)


def _check(column_names: Sequence[str]) -> None:
    """Are the given column names safe-looking?

    The existence of this function is a code smell. Using user-provided data to
    define column names is a *bad idea*. The requirements for CSV files should
    be re-worked so that this function can be deleted.

    :param column_names: A sequence of strings that might be used as column
        names.
    :throw pp.exceptions.DatabaseCPOPError: If any of the given column names
        look even slightly fishy.
    """
    matcher = re.compile(r'^[a-z0-9-_ ]+$')
    for column_name in column_names:
        if not matcher.match(column_name):
            raise exceptions.DatabaseCPOPError(
                f"""
                Illegal column name encountered: {column_name}. Please ensure
                all column names match the regex {matcher}. This requirement
                exists because column names are used when constructing the
                database schema. Abiding by this regex doesn't guarantee that
                column names will be accepted by the underlying database, but
                it does help prevent weird bugs.
                """
            )


def create_means_table(conn: sqlite3.Connection) -> None:
    """Create the :data:`pp.constants.MEANS_TABLE`.

    :param conn: A connection to the target SQLite database.
    """
    with conn:
        conn.execute(
            f"""
            CREATE TABLE {MEANS_TABLE} (
                table_name  TEXT NOT NULL,
                column_name TEXT NOT NULL,
                mean        REAL NOT NULL,
                PRIMARY KEY (table_name, column_name)
            )
            """
        )


def create_std_devs_table(conn: sqlite3.Connection) -> None:
    """Create the :data:`pp.constants.STD_DEVS_TABLE`.

    :param conn: A connection to the target SQLite database.
    """
    with conn:
        conn.execute(
            f"""
            CREATE TABLE {STD_DEVS_TABLE} (
                table_name  TEXT NOT NULL,
                column_name TEXT NOT NULL,
                std_dev     REAL NOT NULL,
                PRIMARY KEY (table_name, column_name)
            )
            """
        )


def create_std_data_tables(conn: sqlite3.Connection) -> None:
    """Create the :data:`pp.constants.STD_DATA_TABLES`.

    :param conn: A connection to the target SQLite database.
    """
    col_names: Sequence[str] = tuple(read.column_names(DATA_TABLES[0]))
    col_types: Sequence[str] = tuple(
        COLUMN_TYPES[read.column_type(col_name)] for col_name in col_names
    )
    col_defs: str = ', '.join(
        f'"{col_name}" {col_type} NOT NULL'
        for col_name, col_type in zip(col_names, col_types)
    )
    with conn:
        for table in STD_DATA_TABLES:
            conn.execute(f'CREATE TABLE {table} ({col_defs})')


def create_models_table(conn: sqlite3.Connection) -> None:
    """Create the :data:`pp.constants.MODELS_TABLE`.

    :param conn: A connection to the target SQLite database.
    """
    with conn:
        conn.execute(
            f"""
            CREATE TABLE {MODELS_TABLE} (
                output_column TEXT NOT NULL PRIMARY KEY,
                cost          REAL NOT NULL,
                offset        REAL NOT NULL,
                input_columns TEXT NOT NULL
            )
            """
        )


def normalize(
        *,
        jobs: Optional[int] = None,
        reporter: Optional[Callable] = None) -> None:
    """Create a normalized copy of :data:`pp.constants.TRAINING_TABLE`.

    :param jobs: The number of processes to spawn. If ``None``, spawn one per
        CPU.
    """
    means(jobs=jobs, reporter=reporter)
    std_devs(jobs=jobs, reporter=reporter)
    std_scores(reporter=reporter)


def means(
        *,
        jobs: Optional[int] = None,
        reporter: Optional[Callable] = None) -> None:
    """Find means for the :data:`pp.constants.TRAINING_TABLE`.

    :param jobs: The number of processes to spawn. If ``None``, spawn one per
        CPU.
    """
    # SQLite3 locks are database-wide. It is most efficient to perform all
    # reads before performing any writes. Thus, the call to tuple(). There are
    # two possible downsides to this approach:
    #
    # * To-be-written data must be buffered in memory. If there is lots of data
    #   to be written, this could balloon memory usage.
    # * If this process is killed, then results which haven't been written are
    #   lost. If results take a long time to calculate, this is an annoyance.
    #
    # These concerns haven't been an issue with the data sizes seen thus far.
    # If they do become an issue, then this function should be rewritten so
    # that chunks of (e.g. 256) results are calculated and written at a time.
    for table_name in DATA_TABLES:
        rows = tuple(calc.means(table_name, jobs=jobs, reporter=reporter))
        write.means(rows)


def std_devs(
        *,
        jobs: Optional[int] = None,
        reporter: Optional[Callable] = None) -> None:
    """Find standard deviations for the :data:`pp.constants.TRAINING_TABLE`.

    .. WARNING:: Means must already have been calculated. See
        :func:`pp.model.means`.

    :param jobs: The number of processes to spawn. If ``None``, spawn one per
        CPU.
    """
    # For reasoning on why tuple() is used, see the comments in means().
    for table_name in DATA_TABLES:
        rows = tuple(calc.std_devs(table_name, jobs=jobs, reporter=reporter))
        write.std_devs(rows)


def std_scores(*, reporter: Optional[Callable] = None) -> None:
    """Find standard scores for the :data:`pp.constants.TRAINING_TABLE`.

    For each cell in a continuous column in the
    :data:`pp.constants.TRAINING_TABLE`, find the corresponding `standard
    score`_ and place it into the :data:`pp.constants.STD_TRAINING_TABLE`.

    .. WARNING:: Standard deviations must already have been calculated. See
        :func:`pp.model.std_devs`.

    .. _standard score: https://en.wikipedia.org/wiki/Standard_score
    """
    # For reasoning on why tuple() is used, see the comments in means().
    for denorm_table_name, norm_table_name in zip(
            DATA_TABLES, STD_DATA_TABLES):
        with common.get_db_conn() as conn:
            with conn:
                conn.execute(f'DELETE FROM {norm_table_name}')
        rows = tuple(calc.std_scores(denorm_table_name, reporter=reporter))
        write.std_scores(norm_table_name, rows)
