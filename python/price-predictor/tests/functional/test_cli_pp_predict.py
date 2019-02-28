# coding=utf-8
"""Functional tests for :mod:`pp.cli.pp_predict`."""
import contextlib
import subprocess
import unittest

from pp import datasets
from pp.constants import TEST_SEED

from .utils import run, temp_xdg_data_home

# pylint:disable=no-self-use
# The unittest framework requires that tests be instance methods.


class HelpFlagTestCase(unittest.TestCase):
    """Ensure the ``--help`` flag works."""

    def test_help(self):
        """Pass ``--help`` to ``pp-model`` and its subcommands."""
        run('pp-predict --help'.split())


class SimpleTestCase(unittest.TestCase):
    """Call ``pp-predict`` with a few arguments, as a sanity check."""

    def setUp(self):
        """Install a dataset, and create and populate the database."""
        with contextlib.ExitStack() as stack:
            stack.enter_context(temp_xdg_data_home())
            self.addCleanup(stack.pop_all().close)
        dataset_name = datasets.FixtureKingCountyDS().name
        self.columns = ('bathrooms', 'price', 'sqft_living')

        run(f'pp-dataset install {dataset_name}'.split())
        run(f'pp-db cpop {dataset_name} --seed {TEST_SEED}'.split())
        run('pp-db normalize'.split())
        run(('pp-model', 'lin-reg') + self.columns)

    def test_positive(self):
        """Perform a sanity check."""
        prefix = ('pp-predict', self.columns[0])
        suffixes = (
            (),
            ('--mean-error',),
            ('--mean-squared-error',),
            ('--median-error',),
            ('--denormalize',),
            ('--denormalize', '--mean-error',),
            ('--denormalize', '--mean-squared-error',),
            ('--denormalize', '--median-error',),
            ('--table', 'development_std_scores'),
            ('--table', 'development_std_scores', '--mean-error',),
            ('--table', 'development_std_scores', '--mean-squared-error',),
            ('--table', 'development_std_scores', '--median-error',),
            ('--table', 'development_std_scores', '--denormalize',),
            ('--table', 'development_std_scores', '--denormalize', '--mean-error',),
            ('--table', 'development_std_scores', '--denormalize', '--mean-squared-error',),
            ('--table', 'development_std_scores', '--denormalize', '--median-error',),
        )
        for suffix in suffixes:
            with self.subTest(suffix=suffix):
                run(prefix + suffix)

    def test_negative(self):
        """Perform a sanity check."""
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-predict', self.columns[1]))
