"""Test how pytest handles nested fixtures."""
# redefined-outer-name is disabled in function signatures to accomodate pytest's fixtures.
from typing import Iterable

import pytest


@pytest.fixture
def inner() -> Iterable[list]:
    """Yield a list, ``["inner"]``, then clear the list during tear-down."""
    target = ["inner"]
    yield target
    target.clear()


@pytest.fixture
def outer(inner) -> list:  # pylint:disable=redefined-outer-name
    """Append an "outer" to ``inner``, then return inner."""
    inner.append("outer")
    return inner


def test_inner(inner) -> None:  # pylint:disable=redefined-outer-name
    """Append an element to ``inner``, then verify its contents."""
    assert isinstance(inner, list)
    inner.append("test_inner")
    assert inner == ["inner", "test_inner"]


def test_outer(outer) -> None:  # pylint:disable=redefined-outer-name
    """Append an item to the outer list."""
    assert isinstance(outer, list)
    outer.append("test_outer")
    assert outer == ["inner", "outer", "test_outer"]
