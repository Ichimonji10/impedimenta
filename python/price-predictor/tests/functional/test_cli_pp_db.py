# coding=utf-8
"""Functional tests for :mod:`pp.cli.pp_dataset`."""
import contextlib
import importlib
import random
import subprocess
import unittest

from xdg import BaseDirectory

from pp import datasets
from pp.constants import TEST_SEED
from pp.db import count, read
from .utils import run, temp_xdg_data_home

# pylint:disable=no-self-use
# The unittest framework requires that tests be instance methods.


class HelpFlagTestCase(unittest.TestCase):
    """Ensure the ``--help`` flag works."""

    def test_help(self):
        """Pass ``--help`` to ``pp-db`` and its subcommands."""
        commands = (
            'pp-db --help'.split(),
            'pp-db load-path --help'.split(),
            'pp-db save-path --help'.split(),
            'pp-db cpop --help'.split(),
            'pp-db normalize --help'.split(),
        )
        for command in commands:
            with self.subTest(command=command):
                run(command)


class NormalizeTestCase(unittest.TestCase):
    """Test the ``normalize`` subcommand."""

    def setUp(self):
        """Install a dataset, and create and populate the database."""
        with contextlib.ExitStack() as stack:
            stack.enter_context(temp_xdg_data_home())
            self.addCleanup(stack.pop_all().close)
        dataset_name = datasets.FixtureSimpleDS().name
        run(f'pp-dataset install {dataset_name}'.split())
        run(f'pp-db cpop {dataset_name} --seed {TEST_SEED}'.split())

    def test_no_flags(self):
        """Normalize the db and pass no flags."""
        run('pp-db normalize'.split())

    def test_progress_flag(self):
        """Normalize the db and pass the ``--progress`` flag."""
        run('pp-db normalize --progress'.split())

    def test_no_progress_flag(self):
        """Normalize the db and pass the ``--no-progress`` flag."""
        run('pp-db normalize --no-progress'.split())

    def test_jobs_flag(self):
        """Normalize the db and pass the ``--jobs`` flag."""
        for jobs in ('1', '2', '4'):
            with self.subTest(jobs=jobs):
                run(f'pp-db normalize --jobs {jobs}'.split())


class FixtureSimpleTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureSimpleDS`."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.dataset = datasets.FixtureSimpleDS()

    @temp_xdg_data_home()
    def test_save_path(self):
        """Test the "save-path" subcommand."""
        paths = run(('pp-db', 'save-path'))
        self.assertEqual(len(paths), 1, paths)
        importlib.reload(BaseDirectory)
        self.assertTrue(
            paths[0].startswith(BaseDirectory.xdg_data_home),
            (paths[0], BaseDirectory.xdg_data_home),
        )

    @temp_xdg_data_home()
    def test_load_path(self):
        """Don't create a database, and run the load-path subcommand.

        Assert it returns non-zero, because no database can be found.
        """
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-db', 'load-path'))

    @temp_xdg_data_home()
    def test_cpop_load_path(self):
        """Do create a database, and run the load-path subcommand.

        Assert it returns zero, because a database is found.
        """
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', self.dataset.name))
        paths = run(('pp-db', 'load-path'))
        self.assertEqual(len(paths), 1, paths)
        importlib.reload(BaseDirectory)
        self.assertTrue(
            paths[0].startswith(BaseDirectory.xdg_data_home),
            (paths[0], BaseDirectory.xdg_data_home),
        )

    @temp_xdg_data_home()
    def test_cpop_false_false_v1(self):
        """Call ``cpop``, ``cpop``.

        Assert the second call fails, because a database is already present.
        """
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', self.dataset.name))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-db', 'cpop', self.dataset.name))

    @temp_xdg_data_home()
    def test_cpop_false_false_v2(self):
        """Call ``cpop --no-overwrite``, ``cpop --no-overwrite``.

        Assert the second call fails, because a database is already present.
        """
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', '--no-overwrite', self.dataset.name))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-db', 'cpop', '--no-overwrite', self.dataset.name))

    @temp_xdg_data_home()
    def test_cpop_false_true(self):
        """Call ``cpop``, ``cpop --overwrite``.

        Assert both commands succeed.
        """
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', self.dataset.name))
        run(('pp-db', 'cpop', '--overwrite', self.dataset.name))

    @temp_xdg_data_home()
    def test_cpop_true_false(self):
        """Call ``cpop --overwrite``, ``cpop``.

        Assert the second call fails, because a database is already present.
        """
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', '--overwrite', self.dataset.name))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-db', 'cpop', self.dataset.name))

    @temp_xdg_data_home()
    def test_cpop_true_true(self):
        """Call ``cpop --overwrite``, ``cpop --overwrite``.

        Assert both commands succeed.
        """
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', '--overwrite', self.dataset.name))
        run(('pp-db', 'cpop', '--overwrite', self.dataset.name))

    @temp_xdg_data_home()
    def test_cpop_true_true_seed(self):
        """Call ``cpop --overwrite --seed`` twice.

        Verify the command produces identically-sized tables each time.
        """
        seed = str(random.randint(0, 2**8 - 1))
        run(('pp-dataset', 'install', self.dataset.name))

        run((
            'pp-db', 'cpop', '--overwrite', '--seed', seed, self.dataset.name
        ))
        table_names = tuple(read.table_names())
        sizes1 = {table: count.rows(table) for table in table_names}

        run((
            'pp-db', 'cpop', '--overwrite', '--seed', seed, self.dataset.name
        ))
        sizes2 = {table: count.rows(table) for table in table_names}

        self.assertEqual(sizes1, sizes2, seed)


class KingCountyFixtureTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureKingCountyDS`."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.dataset = datasets.FixtureKingCountyDS()

    @temp_xdg_data_home()
    def test_cpop(self):
        """Create and populate the database."""
        run(('pp-dataset', 'install', self.dataset.name))
        run(('pp-db', 'cpop', self.dataset.name))


class FixtureColumnNameMismatchDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureColumnNameMismatchDS`."""

    @temp_xdg_data_home()
    def test_cpop(self):
        """Create and populate the database.

        Assert it fails.
        """
        dataset = datasets.FixtureColumnNameMismatchDS()
        run(('pp-dataset', 'install', dataset.name))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-db', 'cpop', dataset.name))
