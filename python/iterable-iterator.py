#!/usr/bin/env python3
# coding=utf-8
"""Demonstrate what an iterable and an iterator are."""
from collections.abc import Iterable, Iterator


def main():
    """Demonstrate what an iterable and an iterator are."""
    # An object which has the __iter__ method is an iterable. It returns an
    # iterator. (Also see __getitem__.)
    iterable = ['a', 'b']
    assert isinstance(iterable, Iterable)

    # An object which has the __next__ method is an iterator. It returns items
    # from the underlying container, and raises StopIteration.
    iterators = [iter(iterable) for _ in range(2)]
    assert isinstance(iterators[0], Iterator)
    assert next(iterators[0]) == 'a'
    assert next(iterators[1]) == 'a'
    assert next(iterators[0]) == 'b'
    assert next(iterators[1]) == 'b'
    try:
        next(iterators[0])
    except StopIteration:
        print('iterator exhausted')
    try:
        next(iterators[0])
    except StopIteration:
        print('iterator still exhausted')


if __name__ == '__main__':
    main()
