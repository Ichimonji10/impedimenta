# coding=utf-8
"""Tests for module ``functional.utils``."""
import os
import unittest
from pathlib import Path

from tests.functional.utils import temp_xdg_data_home


class TempXDGDataHomeTestCase(unittest.TestCase):
    """Test ``temp_xdg_data_home``."""

    def test_context_manager(self):
        """Check whether the function acts correctly as a context manager."""
        old: str = os.environ.get('XDG_DATA_HOME')
        with temp_xdg_data_home() as temp_xdh:
            mid: str = os.environ.get('XDG_DATA_HOME')
        new: str = os.environ.get('XDG_DATA_HOME')

        with self.subTest():
            self.assertNotEqual(old, temp_xdh)
        with self.subTest():
            self.assertNotEqual(old, mid)
        with self.subTest():
            self.assertEqual(old, new)
        with self.subTest():
            self.assertEqual(temp_xdh, mid)
        with self.subTest():
            self.assertNotEqual(temp_xdh, new)
        with self.subTest():
            self.assertNotEqual(mid, new)

    def test_decorator(self):
        """Check whether the function acts correctly as a decorator."""
        old: str = os.environ.get('XDG_DATA_HOME')

        @temp_xdg_data_home()
        def decorated():
            """Return ``$XDG_DATA_HOME``."""
            return os.environ.get('XDG_DATA_HOME')

        mid: str = decorated()
        new: str = os.environ.get('XDG_DATA_HOME')

        with self.subTest():
            self.assertNotEqual(old, mid)
        with self.subTest():
            self.assertEqual(old, new)
        with self.subTest():
            self.assertNotEqual(mid, new)

    def test_cleanup(self):
        """Check whether the temp dir and its contents are cleaned up."""
        with temp_xdg_data_home() as temp_xdh:
            temp_file = Path(temp_xdh, 'foo.txt')
            with open(temp_file, 'w') as handle:
                handle.write('foo')

        self.assertFalse(Path(temp_xdh).exists())
        self.assertFalse(temp_file.exists())
