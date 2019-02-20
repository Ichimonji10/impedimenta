#!/usr/bin/env python3
# coding=utf-8
"""Demonstrate flow of execution when handling exceptions."""


def outer():
    """Call ``inner``."""
    print('outer starting')
    try:
        print('before calling inner')
        inner()
        print('after calling inner')
    except ZeroDivisionError:
        print('exception caught!')
    print('outer ending')


def inner():
    """Raise a ``ZeroDivisonError``."""
    print('inner starting')
    1 / 0
    print('inner ending')


if __name__ == '__main__':
    outer()
