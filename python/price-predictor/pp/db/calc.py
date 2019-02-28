# coding=utf-8
"""Functions for calculating values from the database.

Using multiprocessing to perform the following calculations is difficult.  The
values calculated above are used as read-only caches, and shipping them (via
pickling and unpickling) for every row is horribly inefficient.  Thankfully,
for a dataset as small as the King County house sale data, this isn't an issue.

The multiprocessing done in this module is overkill. It only provides modest
gains, and greater speeds could probably have been achieved by using numpy to
read the entire dataset into memory and performing the calculations with the
relevant numpy methods.

The abortive attempt to parallelize std_scores() was especially interesting.
std_scores() creates several variables, then uses them as read-only caches when
performing calculations. If one wishes to parallelize the function, then for
each row, a process must have access to that row and to the read-only caches.

By default, processes don't share memory. Thus, the procedure above generates a
huge amount of pickling and unpickling work. It is possible to create shared
variables, but that requires a deeper understanding of the multiprocessing
library than I have.

And if you're going to spend hours learning a toolkit for efficient
matrix-oriented numeric calculations… then just learn numpy.
"""
import statistics
import weakref
from multiprocessing import cpu_count, Pool
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import numpy as np

from pp import exceptions, utils
from pp.constants import CONTINUOUS_TYPE, STD_TRAINING_TABLE, TRAINING_TABLE
from pp.db import common, count, read


def mean(table_name: str, column_name: str) -> common.MeansRow:
    """Calculate the mean of a column.

    :param table_name: The target table.
    :param column_name: The target column.
    :return: The mean of the given column in the given table.
    """
    with common.get_db_conn() as conn:
        cursor = conn.execute(f'SELECT {column_name} FROM {table_name}')
        values: Iterator[Union[float, int]] = (row[0] for row in cursor)
        mean_ = statistics.mean(values)
    return common.MeansRow(table_name, column_name, mean_)


class means:  # pylint:disable=invalid-name
    """Calculate the means of continuous columns in a table.

    :param table_name: The target table.
    :param jobs: The number of processes to spawn. If omitted, spawn one per
        CPU.
    :return: An iterator that yields rows.
    """

    def __init__(
            self,
            table_name: str,
            *,
            jobs: Optional[int] = None,
            reporter: Optional[Callable] = None) -> None:
        """Initialize instance variables."""
        # Do **NOT** give finalize() or its arguments any references to self.
        # See: https://docs.python.org/3/library/weakref.html#weakref.finalize
        self.jobs: int = jobs if jobs else cpu_count()
        pool = Pool(jobs)
        weakref.finalize(self, self.__cleanup, pool)

        # Configure pool to do work.
        func = self._call_mean
        column_names = tuple(read.meta_column_names(CONTINUOUS_TYPE))
        iterable = ((table_name, column_name) for column_name in column_names)
        self.pool_mapper = pool.imap_unordered(func, iterable)

        # Track work done by pool.
        self.numerator: int = 0
        self.press_secretary: Optional[utils.PressSecretary]
        if reporter:
            self.press_secretary = utils.PressSecretary(
                reporter,
                len(column_names),
                f'Calculating means for {table_name}: ',
            )
        else:
            self.press_secretary = None

    def __iter__(self) -> Iterator[common.MeansRow]:
        """Return an iterator that returns means."""
        return self

    def __next__(self) -> common.MeansRow:
        """Calculate and return a mean."""
        try:
            means_row = next(self.pool_mapper)
        except StopIteration:
            if self.press_secretary:
                self.press_secretary.update(self.numerator)
            raise
        if self.press_secretary:
            self.numerator += 1
            # Inversely scale reporting frequency by number of workers so as to
            # avoid flooding the UI.
            if self.numerator % self.jobs == 0:
                self.press_secretary.update(self.numerator)
        return means_row

    @staticmethod
    def __cleanup(pool) -> None:
        pool.terminate()
        pool.join()

    @staticmethod
    def _call_mean(args: Tuple[str, str]) -> common.MeansRow:
        """Call :func:`pp.db.calc.mean`.

        :param args: Passed in to the wrapped function as positional arguments.
        :return: A row suitable for being written to the database.
        """
        return mean(*args)


def std_dev(table_name: str, column_name: str) -> common.StdDevsRow:
    """Calculate the sample standard deviation of a column.

    :param table_name: The table to read.
    :param column_name: The column to read.
    :return: The sample standard deviation of the given column in  the given
        table.
    """
    mean_ = read.mean(table_name, column_name)
    with common.get_db_conn() as conn:
        cursor = conn.execute(f'SELECT {column_name} FROM {table_name}')
        values: Iterator[Union[float, int]] = (row[0] for row in cursor)
        std_dev_ = statistics.stdev(values, mean_)
    return common.StdDevsRow(table_name, column_name, std_dev_)


class std_devs:  # pylint:disable=invalid-name
    """Calc the sample standard deviations of continuous columns in a table.

    :param table_name: The target table.
    :param jobs: The number of processes to spawn. If omitted, spawn one per
        CPU.
    :return: An iterator that yields rows.
    """

    def __init__(
            self,
            table_name: str,
            *,
            jobs: Optional[int] = None,
            reporter: Optional[Callable] = None) -> None:
        """Initialize instance variables."""
        # Do **NOT** give finalize() or its arguments any references to self.
        # See: https://docs.python.org/3/library/weakref.html#weakref.finalize
        self.jobs: int = jobs if jobs else cpu_count()
        pool = Pool(jobs)
        weakref.finalize(self, self.__cleanup, pool)

        # Configure pool to do work.
        func = self._call_std_dev
        column_names = tuple(read.meta_column_names(CONTINUOUS_TYPE))
        iterable = ((table_name, column_name) for column_name in column_names)
        self.pool_mapper = pool.imap_unordered(func, iterable)

        # Track work done by pool.
        self.numerator: int = 0
        self.press_secretary: Optional[utils.PressSecretary]
        if reporter:
            self.press_secretary = utils.PressSecretary(
                reporter,
                len(column_names),
                f'Calculating sample standard deviations for {table_name}: ',
            )
        else:
            self.press_secretary = None

    def __iter__(self) -> Iterator[common.StdDevsRow]:
        """Return an iterator that returns sample standard deviations."""
        return self

    def __next__(self) -> common.StdDevsRow:
        """Calculate and return a sample standard deviation."""
        try:
            std_devs_row = next(self.pool_mapper)
        except StopIteration:
            if self.press_secretary:
                self.press_secretary.update(self.numerator)
            raise
        if self.press_secretary:
            self.numerator += 1
            # Inversely scale reporting frequency by number of workers so as to
            # avoid flooding the UI.
            if self.numerator % self.jobs == 0:
                self.press_secretary.update(self.numerator)
        return std_devs_row

    @staticmethod
    def __cleanup(pool) -> None:
        pool.terminate()
        pool.join()

    @staticmethod
    def _call_std_dev(args: Tuple[str, str]) -> common.StdDevsRow:
        """Call :func:`pp.db.calc.std_dev`.

        :param args: Passed in to the wrapped function as positional arguments.
        :return: A row suitable for being written to the database.
        """
        return std_dev(*args)


class std_scores:  # pylint:disable=invalid-name
    """Walk through a table one row at a time, and return normalized copies.

    Walk through each row of the given table. For each row, make a copy, modify
    the copy, and yield the copy. Modifying the copy consists of walking
    through each cell and doing the following:

    *   If the cell belongs to a categorical column, do nothing.
    *   If the cell belongs to a continuous column, replace the cell with its
        `standard score`_.

    :param table_name: The target table. One of
        :data:`pp.constants.DATA_TABLES`.

    .. _standard score: https://en.wikipedia.org/wiki/Standard_score
    """

    def __init__(
            self,
            table_name: str,
            *,
            reporter: Optional[Callable] = None) -> None:
        """Initialize instance variables."""
        # row:          (-1, 20, 'down', 'orange')
        # col_names:    ('one', 'two', 'three', 'fo ur')
        # col_types:    {'one': CONTINUOUS_TYPE, 'three': CATEGORICAL_TYPE, …}
        # col_means:    {'one': -0.333, 'two': 38.333}
        # col_std_devs: {'one': 2.16, 'two': 23.17}
        self.rows: Iterator = read.table(table_name)
        self.col_names: Iterable[str] = tuple(
            read.column_names(TRAINING_TABLE)
        )
        self.col_types: Mapping[str, str] = {
            col_name: read.column_type(col_name)
            for col_name in self.col_names
        }
        self.col_means: Mapping[str, float] = {
            col_name: read.mean(table_name, col_name)
            for col_name in self.col_names
            if self.col_types[col_name] == CONTINUOUS_TYPE
        }
        self.col_std_devs: Mapping[str, float] = {
            col_name: read.std_dev(table_name, col_name)
            for col_name in self.col_names
            if self.col_types[col_name] == CONTINUOUS_TYPE
        }

        # Reporting machinery.
        self.numerator = 0
        self.press_secretary: Optional[utils.PressSecretary]
        if reporter:
            self.press_secretary = utils.PressSecretary(
                reporter,
                count.rows(table_name),
                f'Calculating standard scores for {table_name}: ',
            )
        else:
            self.press_secretary = None

    def __iter__(self):
        return self

    def __next__(self):
        try:
            denorm_row: Iterator[Any] = next(self.rows)
        except StopIteration:
            if self.press_secretary:
                self.press_secretary.update(self.numerator)
            raise

        norm_row: List[Union[float, str]] = []
        norm_cell: Union[float, str]
        for cell, col_name in zip(denorm_row, self.col_names):
            if self.col_types[col_name] == CONTINUOUS_TYPE:
                try:
                    norm_cell = (
                        (cell - self.col_means[col_name]) /
                        self.col_std_devs[col_name]
                    )
                except ZeroDivisionError:
                    # As an example, the continuous "view" column in the
                    # fixture-king-county dataset consists entirely of
                    # zeroes. In this case, the standard deviation is zero.
                    norm_cell = 0
            else:
                norm_cell = cell
            norm_row.append(norm_cell)

        if self.press_secretary:
            self.numerator += 1
            if self.numerator % 2**8 == 0:
                self.press_secretary.update(self.numerator)

        return norm_row


def model(
        out_col_name: str,
        in_cols_names: Sequence[str],
        lambda_: float) -> common.ModelsRow:
    """Model a dependent column with independent columns.

    :param out_col_name: The column to predict.
    :param in_cols_names: The columns to use to formulate a model.
    :param lambda_: See :data:`pp.constants.LAMBDA`.
    :return: A least-squares linear matrix equation.
    :raise pp.exceptions.ModelingError: If unable to create a model.
    """
    # A column consisting of all ones has been appended to in_cols.
    out_col = np.array(
        tuple(
            row[0] for row in read.table(STD_TRAINING_TABLE, (out_col_name,))
        ),
        np.float_,
    )
    in_cols = np.array(
        tuple(_read_with_extra_col(STD_TRAINING_TABLE, in_cols_names)),
        np.float_,
    )

    # coefs: coefficients of in_cols. sses: sum of squared errors, where errors
    # are differences between predicted outputs and out_col.
    coefs, sses, _, _ = np.linalg.lstsq(in_cols, out_col, None)

    # cost of model = error(model) + λ × complexity(model)
    try:
        error = sses[0] / len(out_col)
    except IndexError:
        raise exceptions.ModelingError(
            f"Can't model {out_col_name} with {in_cols_names}. Maybe the "
            'input columns are insufficiently independent, or too few rows '
            'are present.'
        )
    cost: float = error + lambda_ * len(in_cols_names)

    # Associate coefficients with synthetic column and input columns.
    assert len(in_cols_names) == len(coefs) - 1
    offset: float = coefs[-1]
    in_cols_names_coefs: Mapping[str, float] = {
        input_col: coef for input_col, coef in zip(in_cols_names, coefs)
    }

    return common.ModelsRow(out_col_name, cost, offset, in_cols_names_coefs)


class models:  # pylint:disable=invalid-name
    """Model an output column with sets of input columns.

    :param out_col_name: Same as for :func:`pp.db.calc.model`.
    :param in_cols_names: Same as for :func:`pp.db.calc.model`.
    :param lambda_: Same as for :func:`pp.db.calc.model`.
    :param combinations: Model varying combinations of the input columns. For
        example, if the input columns are a and b, then columns [a, b], [a],
        and [b] would be modeled.
    :param jobs: The number of processes to spawn. If omitted, spawn one per
        CPU.
    :return: Same as for :func:`pp.db.calc.model`, but an iterable thereof.
    """

    def __init__(
            self,
            out_col_name: str,
            in_cols_names: Sequence[str],
            lambda_: float,
            combinations: bool = False,
            *,
            jobs: Optional[int] = None,
            reporter: Optional[Callable] = None) -> None:
        """Initialize instance variables."""
        # Do **NOT** give finalize() or its arguments any references to self.
        # See: https://docs.python.org/3/library/weakref.html#weakref.finalize
        self.jobs: int = jobs if jobs else cpu_count()
        pool = Pool(jobs)
        weakref.finalize(self, self.__cleanup, pool)

        # Configure pool to do work.
        func = self._call_model
        iterable = (
            (out_col_name, in_cols_names, lambda_)
            for in_cols_names
            in self._in_cols_names_iter(in_cols_names, combinations)
        )
        self.pool_mapper = pool.imap_unordered(func, iterable)

        # Track work done by pool.
        self.numerator: int = 0
        self.press_secretary: Optional[utils.PressSecretary]
        if reporter:
            denominator = 2 ** len(in_cols_names) - 1 if combinations else 1
            self.press_secretary = utils.PressSecretary(
                reporter,
                denominator,
                f'Modeling {out_col_name} with {denominator} models: ',
            )
        else:
            self.press_secretary = None

    def __iter__(self) -> Iterator[common.ModelsRow]:
        """Return an iterator that returns models."""
        return self

    def __next__(self) -> common.ModelsRow:
        """Calculate and return a model."""
        models_row: Optional[common.ModelsRow] = None
        while not models_row:
            # skip None values
            try:
                models_row = next(self.pool_mapper)
            except StopIteration:
                if self.press_secretary:
                    self.press_secretary.update(self.numerator)
                raise
            if self.press_secretary:
                self.numerator += 1
                # Inversely scale reporting frequency by number of workers so as to
                # avoid flooding the UI.
                if self.numerator % self.jobs == 0:
                    self.press_secretary.update(self.numerator)
        return models_row

    @staticmethod
    def _in_cols_names_iter(
            in_cols_names: Sequence[str],
            combinations: bool) -> Iterator[Sequence[str]]:
        """Create an iterator of input columns.

        If ``combinations``, let the iterator return sequences of
        ``in_cols_names`` as produced by :func:`pp.utils.varying_combinations`.
        Otherwise, let the iterator return a single sequence consisting of
        ``in_cols_names``.
        """
        in_cols_names_iterable: Iterable[Sequence[str]]
        if combinations:
            in_cols_names_iterable = utils.varying_combinations(in_cols_names)
        else:
            in_cols_names_iterable = (in_cols_names,)
        return iter(in_cols_names_iterable)

    @staticmethod
    def __cleanup(pool) -> None:
        pool.terminate()
        pool.join()

    @staticmethod
    def _call_model(args) -> Optional[common.ModelsRow]:
        """Call :func:`pp.db.calc.mean`.

        :param args: Passed in to the wrapped function as positional arguments.
        :return: Same as the wrapped function, except that if a
            :class:`pp.exceptions.ModelingError` occurs, ``None`` will be returned.
        """
        try:
            return model(*args)
        except exceptions.ModelingError:
            return None


def _read_with_extra_col(*args, **kwargs):
    for row in read.table(*args, **kwargs):
        yield tuple(row) + (1,)
