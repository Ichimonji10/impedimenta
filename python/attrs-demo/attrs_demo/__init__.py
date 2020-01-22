# coding=utf-8
"""Explore some aspects of the `attrs`_ package.

.. _attrs: http://www.attrs.org/en/stable/index.html
"""
import attr

__version__ = '0.1.0'


def main():
    """Instantiate and print a ``Klass``."""
    klass = Klass('a', 'b')
    print(f'repr(klass): {repr(klass)}')
    print(f'str(klass): {str(klass)}')
    print(f'klass.class_attrib: {klass.class_attrib}')
    print(f'Klass.class_attrib: {Klass.class_attrib}')


@attr.s
class Klass:
    """A simple data-only class.

    ``bare``
        Required. No default value.

    ``nothing``
        Required. No default value.

    ``none``
        Optional. Default value.

    ``class_attrib``
        Not defined with ``attr``, so not included in ``repr()`` or ``str()``.
    """
    bare = attr.ib()
    nothing = attr.ib(default=attr.NOTHING)
    none = attr.ib(default=None)
    class_attrib = 'class attribute'
