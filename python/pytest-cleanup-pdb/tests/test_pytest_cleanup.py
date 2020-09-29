import pytest
from typing import Generator


@pytest.fixture(scope="function")
def before_and_after() -> Generator[str, None, None]:
    print("SET-UP WORK")
    yield "SPECIAL YIELDED VALUE"
    print("TEAR-DOWN WORK")


def test_foo(before_and_after: str) -> None:
    print(before_and_after)
    assert 0
