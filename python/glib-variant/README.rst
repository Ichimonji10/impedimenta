GLib Variant
============

A simple set of tests for the GLib variant type.

A GLib variant may hold a varying underlying tupe, such as a signed 64-bit
integer (int64), an unsigned 64-bit integer (uint64), or so on. Variants are
useful in several situations, one of which is when serializing data to send it
across DBus.

What happens if one attempts to place an inappropriate value inside a variant?
Ideally, GLib would notice the error and respond with an exception. This module
contains several unit tests which aim to find out. For example, one valid GLib
variant data type is the guint16, which can hold integers in the range 0–65535,
or 0 to 2^16 - 1. Will GLib reject a guint16 variant with a value of -1 or
65536?

To run the tests, execute:

.. code-block:: sh

    python -m unittest main.py
