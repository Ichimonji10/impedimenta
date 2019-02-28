# coding=utf-8
"""Functional tests for :mod:`pp.dataset`."""
import contextlib
import statistics
import unittest
from typing import List

from pp import datasets, exceptions
from pp.constants import STD_TRAINING_TABLE, TEST_SEED, TRAINING_TABLE
from pp.db import count, init, read
from .utils import temp_xdg_data_home

# pylint:disable=no-self-use
# The unittest framework requires that tests be instance methods.


class FixtureColumnNameMismatchDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureColumnNameMismatchDS`."""

    @temp_xdg_data_home()
    def test_cpop(self):
        """Create and populate the database.

        Assert it fails.
        """
        dataset = datasets.FixtureColumnNameMismatchDS()
        dataset.install()
        with self.assertRaises(exceptions.DatabaseCPOPError):
            init.cpop_db(dataset.name)


class NormalizeTestCase(unittest.TestCase):
    """Normalize the testing table, and verify the results."""

    def setUp(self):
        """Install a dataset, and create, populate and normalize the db."""
        with contextlib.ExitStack() as stack:
            stack.enter_context(temp_xdg_data_home())
            self.addCleanup(stack.pop_all().close)
        dataset = datasets.FixtureSimpleDS()
        dataset.install()
        init.cpop_db(dataset.name, TEST_SEED)
        init.normalize()

        self.training_table = {
            'one': (0, 1),
            'two': (30, 40),
            'three': ('right', 'left'),
            'fo ur': ('yellow', 'green'),
        }

    def test_means(self):
        """Verify means."""
        for col_name in ('one', 'two'):
            with self.subTest(col_name=col_name):
                target = statistics.mean(self.training_table[col_name])
                actual = read.mean(TRAINING_TABLE, col_name)
                self.assertEqual(target, actual)

        for col_name in ('three', 'fo ur'):
            with self.subTest(col_name=col_name):
                with self.assertRaises(exceptions.MissingValueError):
                    read.mean(TRAINING_TABLE, col_name)

    def test_std_devs(self):
        """Verify standard deviations."""
        for col_name in ('one', 'two'):
            with self.subTest(col_name=col_name):
                target = statistics.stdev(self.training_table[col_name])
                actual = read.std_dev(TRAINING_TABLE, col_name)
                self.assertEqual(target, actual)

        for col_name in ('three', 'fo ur'):
            with self.subTest(col_name=col_name):
                with self.assertRaises(exceptions.MissingValueError):
                    read.mean(TRAINING_TABLE, col_name)

    def test_std_scores(self):
        """Verify standard scores."""
        means = {
            col_name: read.mean(TRAINING_TABLE, col_name)
            for col_name in ('one', 'two')
        }
        std_devs = {
            col_name: read.std_dev(TRAINING_TABLE, col_name)
            for col_name in ('one', 'two')
        }

        # This is what should be stored in the database.
        target_cols = {
            'one': tuple((
                (cell - means['one']) / std_devs['one']
                for cell in self.training_table['one']
            )),
            'two': tuple((
                (cell - means['two']) / std_devs['two']
                for cell in self.training_table['two']
            )),
            'three': self.training_table['three'],
            'fo ur': self.training_table['fo ur'],
        }

        # This is what's actually stored in the database.
        actual_cols = {
            'one': tuple(
                row[0] for row in read.table(STD_TRAINING_TABLE, ('one',))),
            'two': tuple(
                row[0] for row in read.table(STD_TRAINING_TABLE, ('two',))),
            'three': tuple(
                row[0] for row in read.table(STD_TRAINING_TABLE, ('three',))),
            'fo ur': tuple(
                row[0] for row in read.table(STD_TRAINING_TABLE, ('fo ur',))),
        }

        for col_name in target_cols:
            with self.subTest(col_name=col_name):
                self.assertEqual(target_cols[col_name], actual_cols[col_name])

    def test_normalize_twice(self):
        """Normalize the database twice.

        Assert the table into which scores are written is the same size after
        each normalization. If it grows, then the target table isn't being
        cleared during each normalization.
        """
        sizes: List[int] = []
        sizes.append(count.rows(STD_TRAINING_TABLE))
        init.normalize()
        sizes.append(count.rows(STD_TRAINING_TABLE))
        self.assertEqual(*sizes)  # pylint:disable=no-value-for-parameter


class FixtureKingCountyTestCase(unittest.TestCase):
    """Normalize the :class:`pp.datasets.FixtureKingCountyDS`.

    A bit of work is necessary to import the King County dataset into the
    database. Import it and perform some basic analyses to ensure that the
    import logic is correct.
    """

    @temp_xdg_data_home()
    def test_all(self):
        """Calculate standard deviations."""
        dataset = datasets.FixtureKingCountyDS()
        dataset.install()
        init.cpop_db(dataset.name, TEST_SEED)
        init.normalize()
