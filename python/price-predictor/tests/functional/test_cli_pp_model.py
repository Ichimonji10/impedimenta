# coding=utf-8
"""Functional tests for :mod:`pp.cli.pp_model`."""
import contextlib
import subprocess
import unittest

from pp import datasets
from pp.constants import CONTINUOUS_TYPE, TEST_SEED
from pp.db import read
from .utils import run, temp_xdg_data_home

# pylint:disable=no-self-use
# The unittest framework requires that tests be instance methods.


class HelpFlagTestCase(unittest.TestCase):
    """Ensure the ``--help`` flag works."""

    def test_help(self):
        """Pass ``--help`` to ``pp-model`` and its subcommands."""
        commands = (
            'pp-model --help'.split(),
            'pp-model modelable --help'.split(),
            'pp-model lin-reg --help'.split(),
        )
        for command in commands:
            with self.subTest(command=command):
                run(command)


class LinRegTestCase(unittest.TestCase):
    """Test the ``lin-reg`` subcommand."""

    def setUp(self):
        """Install a dataset, and create and populate the database."""
        with contextlib.ExitStack() as stack:
            stack.enter_context(temp_xdg_data_home())
            self.addCleanup(stack.pop_all().close)
        dataset_name = datasets.FixtureKingCountyDS().name
        run(f'pp-dataset install {dataset_name}'.split())
        run(f'pp-db cpop {dataset_name} --seed {TEST_SEED}'.split())
        run('pp-db normalize'.split())
        self.columns = ('bathrooms', 'price', 'sqft_living')

    def test_no_flags(self):
        """Don't pass any flags."""
        run(('pp-model', 'lin-reg') + self.columns)

    def test_combinations_flag(self):
        """Pass the ``--combinations`` flag."""
        run(('pp-model', 'lin-reg') + self.columns + ('--combinations',))

    def test_lambda_flag(self):
        """Pass the ``--lambda`` flag."""
        run(('pp-model', 'lin-reg') + self.columns + ('--lambda', '0.5'))

    def test_lambda_flag_v2(self):
        """Pass the ``--lambda`` flag with an invalid value."""
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-model', 'lin-reg') + self.columns + ('--lambda', 'foo'))

    def test_jobs_flag(self):
        """Pass the ``--jobs`` flag."""
        run(('pp-model', 'lin-reg') + self.columns + ('--jobs', '2'))

    def test_progress_flag(self):
        """Pass the ``--progress`` flag."""
        run(('pp-model', 'lin-reg') + self.columns + ('--progress',))

    def test_predict_self(self):
        """Use a column to predict itself.

        Assert an error occurs.
        """
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-model', 'lin-reg') + self.columns + (self.columns[0],))

    def test_predict_redundant(self):
        """Use a column twice.

        Assert an error occurs.
        """
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-model', 'lin-reg') + self.columns + (self.columns[-1],))

    @unittest.skip(
        """
        It is impossible to model all of fixture-king-county's columns. This is
        because certain columns are filled with homogenous values, like all
        zeroes. This causes the relevant matrix math to fail.
        """)
    def test_no_output_cols(self):
        """Don't specify any output columns."""
        run(('pp-model', 'lin-reg', self.columns[0]))


class ModelableTestCase(unittest.TestCase):
    """Test the ``modelable`` subcommand."""

    @temp_xdg_data_home()
    def test_no_flags(self):
        """Don't pass any flags."""
        dataset_name = datasets.FixtureSimpleDS().name
        run(f'pp-dataset install {dataset_name}'.split())
        run(f'pp-db cpop {dataset_name} --seed {TEST_SEED}'.split())
        run('pp-db normalize'.split())
        actual = set(run('pp-model modelable'.split()))
        target = set(read.meta_column_names(CONTINUOUS_TYPE))
        self.assertEqual(actual, target)
