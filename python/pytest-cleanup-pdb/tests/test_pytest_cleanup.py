"""Tests demonstrating the interation between fixture tear-down and ``--pdb``.

See the root-level readme file for more information.
"""
from typing import Generator

import pytest


@pytest.fixture(scope="function")
def before_and_after() -> Generator[str, None, None]:
    """Yield a string.

    Print distinct messages to stdout both before andafter yielding.
    """
    print("SET-UP WORK")
    yield "SPECIAL YIELDED VALUE"
    print("TEAR-DOWN WORK")


# pytest figures out which fixtures to invoke based on argument names. It's a bizarre design that is
# both opaque and that forces name re-definitions.
def test_foo(before_and_after: str) -> None:  # pylint:disable=redefined-outer-name
    """Print the passed-in fixture, then make a failing assertion."""
    print(before_and_after)
    assert 0
