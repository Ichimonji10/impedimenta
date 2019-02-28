# coding=utf-8
"""Functional tests for :mod:`pp.cli.pp_dataset`."""
import importlib
import subprocess
import unittest

from xdg import BaseDirectory

from pp import datasets
from .utils import run, temp_xdg_data_home


class HelpTestCase(unittest.TestCase):
    """Ensure the ``--help`` flags work."""

    def test_help(self):
        """Pass ``--help`` to ``pp-dataset`` and its subcommands."""
        commands = (
            'pp-dataset --help'.split(),
            'pp-dataset install --help'.split(),
            'pp-dataset installed --help'.split(),
            'pp-dataset manageable --help'.split(),
            'pp-dataset uninstall --help'.split(),
        )
        for command in commands:
            with self.subTest(command=command):
                run(command)


class FixtureSimpleDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureSimpleDS`."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.dataset = datasets.FixtureSimpleDS()

    @temp_xdg_data_home()
    def test_manageable(self):
        """Test the "manageable" subcommand."""
        stdout = run(('pp-dataset', 'manageable'))
        self.assertIn(self.dataset.name, stdout)

    @temp_xdg_data_home()
    def test_install_uninstall(self):
        """Test install, uninstall, and installed subcommands.

        Do the following for this class' dataset:

        #.  Assert the dataset is not installed.
        #.  Install the dataset. Assert the dataset is installed, and that it
            is located in a sane-looking place.
        #.  Uninstall the dataset. Assert the dataset is not installed.
        """
        paths = run(('pp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 0, paths)

        run(('pp-dataset', 'install', self.dataset.name))
        paths = run(('pp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 1, paths)
        importlib.reload(BaseDirectory)
        self.assertTrue(
            paths[0].startswith(BaseDirectory.xdg_data_home),
            (paths[0], BaseDirectory.xdg_data_home),
        )

        run(('pp-dataset', 'uninstall', self.dataset.name))
        paths = run(('pp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 0, paths)

    @temp_xdg_data_home()
    def test_install_installed_cli(self):
        """Install an already-installed dataset."""
        run(('pp-dataset', 'install', self.dataset.name))
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-dataset', 'install', self.dataset.name))

    @temp_xdg_data_home()
    def test_uninstall_uninstalled(self):
        """Uninstall an already-uninstalled dataset."""
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-dataset', 'uninstall', self.dataset.name))


class FixtureKingCountyDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureKingCountyDS`."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.dataset = datasets.FixtureKingCountyDS()

    @temp_xdg_data_home()
    def test_install_uninstall(self):
        """Install and uninstall the dataset."""
        paths = run(('pp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 0, paths)

        run(('pp-dataset', 'install', self.dataset.name))
        paths = run(('pp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 1, paths)

        run(('pp-dataset', 'uninstall', self.dataset.name))
        paths = run(('pp-dataset', 'installed', '--path'))
        self.assertEqual(len(paths), 0, paths)


class FixtureKingCountyMalformedDateDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureKingCountyMalformedDateDS`."""

    @temp_xdg_data_home()
    def test_install(self):
        """Install this dataset.

        Installation should fail, as the dataset has a malformed date.
        """
        dataset = datasets.FixtureKingCountyMalformedDateDS()
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-dataset', 'install', dataset.name))


class FixtureMissingFileDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureMissingFileDS`."""

    @temp_xdg_data_home()
    def test_install(self):
        """Install the dataset.

        Installation should fail, as the dataset is missing ``metadata.csv``.
        """
        dataset = datasets.FixtureMissingFileDS()
        with self.assertRaises(subprocess.CalledProcessError):
            run(('pp-dataset', 'install', dataset.name))
