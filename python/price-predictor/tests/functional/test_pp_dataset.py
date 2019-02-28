# coding=utf-8
"""Functional tests for :mod:`pp.dataset`."""
import unittest

from pp import datasets, exceptions
from .utils import temp_xdg_data_home


class FixtureSimpleDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureSimpleDS`."""

    @classmethod
    def setUpClass(cls):
        """Create class-wide variables."""
        cls.dataset = datasets.FixtureSimpleDS()

    @temp_xdg_data_home()
    def test_install_installed_api(self):
        """Install an already installed dataset."""
        self.dataset.install()
        with self.assertRaises(exceptions.DatasetInstallError):
            self.dataset.install()

    @temp_xdg_data_home()
    def test_uninstall_uninstalled(self):
        """Uninstall an already-uninstalled dataset."""
        with self.assertRaises(exceptions.DatasetNotFoundError):
            self.dataset.uninstall()


class FixtureKingCountyMalformedDateDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureKingCountyMalformedDateDS`."""

    @temp_xdg_data_home()
    def test_install(self):
        """Install this dataset.

        Installation should fail, as the dataset has a malformed date.
        """
        dataset = datasets.FixtureKingCountyMalformedDateDS()
        with self.assertRaises(exceptions.DatasetInstallError):
            dataset.install()

class FixtureMissingFileDSTestCase(unittest.TestCase):
    """Tests for :class:`pp.datasets.FixtureMissingFileDS`."""

    @temp_xdg_data_home()
    def test_install_api(self):
        """Install the dataset.

        Installation should fail, as the dataset is missing ``metadata.csv``.
        """
        dataset = datasets.FixtureMissingFileDS()
        with self.assertRaises(FileNotFoundError):
            dataset.install()
