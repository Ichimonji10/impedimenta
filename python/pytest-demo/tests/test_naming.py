# coding=utf-8
"""Explore how naming affects test discovery with pytest.

Tests which contain an ``assert False`` will fail if they run.
"""


def test_one() -> None:
    """Function with "test" at the beginning of its name."""
    assert True


def two_test() -> None:
    """Function with "test" at the end of its name."""
    assert False


def three() -> None:
    """Function without "test" in its name."""
    assert False


class TestClass:
    """Class with "test" at the beginning of its name."""

    def test_one(self) -> None:  # pylint:disable=no-self-use
        """Instance method with "test" at the beginning of its name."""
        assert True

    def two_test(self) -> None:  # pylint:disable=no-self-use
        """Instance method with "test" at the end of its name."""
        assert False

    def three(self) -> None:  # pylint:disable=no-self-use
        """Instance method without "test" in its name."""
        assert False

    @classmethod
    def test_four(cls) -> None:
        """Class method with "test" at the beginning of its name."""
        assert False

    @classmethod
    def five_test(cls) -> None:
        """Class method with "test" at the end of its name."""
        assert False

    @classmethod
    def six(cls) -> None:
        """Class method without "test" in its name."""
        assert False

    @staticmethod
    def test_seven() -> None:
        """Static method with "test" at the beginning of its name."""
        assert True

    @staticmethod
    def eight_test() -> None:
        """Static method with "test" at the end of its name."""
        assert False

    @staticmethod
    def nine() -> None:
        """Static method without "test" in the name."""
        assert False


class ClassTest:  # pylint:disable=too-few-public-methods
    """Class with "test" at the end of its name."""

    def test_one(self) -> None:  # pylint:disable=no-self-use
        """Instance method with "test" at the beginning of its name."""
        assert False


class GenericClass:  # pylint:disable=too-few-public-methods
    """Class without "test" in its name."""

    def test_one(self) -> None:  # pylint:disable=no-self-use
        """Instance method with "test" at the beginning of its name."""
        assert False
