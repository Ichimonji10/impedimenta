# coding=utf-8
"""Tests for the GLib variant data type."""
import unittest

import gi
gi.require_version('Gtk', '3.0')  # pylint:disable=wrong-import-position
from gi.repository import GLib


class GLibVariantTestCase(unittest.TestCase):
    """Place values in GLib's variant data type.

    These tests assume knowledge of `GVariant Format Strings
    <https://developer.gnome.org/glib/stable/gvariant-format-strings.html>`_.
    """

    def test_valid_guint16(self):
        """Place valid values into a guint16."""
        for value in (0, 2**16 - 1):
            with self.subTest(value=value):
                variant = GLib.Variant('q', value)
                self.assertEqual(value, variant.unpack())

    def test_invalid_guint16(self):
        """Place invalid values into a guint16."""
        for value in (-1, 2**16):
            with self.subTest(value=value):
                with self.assertRaises(OverflowError):
                    GLib.Variant('q', value)

    def test_valid_string(self):
        """Place valid values into a string."""
        for value in ('', 'a', 'bcd'):
            with self.subTest(value=value):
                variant = GLib.Variant('s', value)
                self.assertEqual(value, variant.unpack())

    def test_invalid_string(self):
        """Place invalid values into a string."""
        for value in (False, True, -1, 0, 1, []):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    GLib.Variant('s', value)

    def test_valid_boolean(self):
        """Place valid values into a gboolean.

        .. NOTE:: This test shows that non-boolean values are cast to a boolean
            when placed into a gboolean GLib variant.
        """
        for value in (False, True, 0, 1, 'False', 'True', -1, 2, []):
            with self.subTest(value=value):
                variant = GLib.Variant('b', value)
                self.assertEqual(bool(value), variant.unpack())

    def test_valid_tuple(self):
        """Place valid values into a tuple variant."""
        value = (False, True)
        variant = GLib.Variant('(bb)', value)
        self.assertEqual(value, variant.unpack())

    def test_invalid_tuple(self):
        """Place invalid values into a tuple variant."""
        with self.assertRaises(TypeError):
            GLib.Variant('(bb)', (False, True, False))
