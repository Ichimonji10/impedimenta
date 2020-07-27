"""Demonstrate the basic usage of autouse fixtures.

The example tests in this module are adapted from `Autouse fixtures (xUnit setup on steroids)`_.
After writing these test cases, my understanding is that a method which is marked with
``@pytest.fixture(autouse=True)`` will be applied to all test methods within its scope.

.. _Autouse fixtures (xUnit setup on steroids):
    https://docs.pytest.org/en/latest/fixture.html#autouse-fixtures-xunit-setup-on-steroids
"""
import pytest

# pylint:disable=redefined-outer-name
# pytest requires that parameter names match fixture names. 🙄


class Database:
    """A mock database that can begin and end transactions."""

    def __init__(self):
        """Set instance variables."""
        self.intransaction = []

    def begin(self, name):
        """Begin a transaction named ``name``."""
        self.intransaction.append(name)

    def end(self):
        """End the most recent transaction."""
        self.intransaction.pop()


@pytest.fixture(scope="module")
def database():
    """Return a ``Database`` object."""
    return Database()


class TestWithoutAutouse:
    """A class that doesn't use an autouse fixture."""

    @staticmethod
    def test_method_1(database):
        """Assert that the database has no transactions."""
        assert not database.intransaction

    @staticmethod
    def test_method_2(database):
        """Assert that the database has no transactions."""
        assert not database.intransaction


class TestWithAutouse:
    """A class that uses an autouse fixture."""

    @pytest.fixture(autouse=True)
    def transact(self, request, database):  # pylint:disable=no-self-use
        """Begin a database transaction before the test starts, and end afterwards."""
        database.begin(request.function.__name__)
        yield
        database.end()

    @staticmethod
    def test_method_1(database):
        """Assert that the database has only one transaction: ``test_method_1``."""
        assert database.intransaction == ["test_method_1"]

    @staticmethod
    def test_method_2(database):
        """Assert that the database has only one transaction: ``test_method_2``."""
        assert database.intransaction == ["test_method_2"]


class TestWithAutouseAndNoDatabase:
    """A class that uses an autouse fixture and no (mock) database."""

    executed = []

    @pytest.fixture(autouse=True)
    def my_autouse(self, request):
        """Append to ``self.executed``."""
        self.executed.append(request.function.__name__)

    def test_method_1(self):
        """Check the contents of ``self.executed``."""
        assert self.executed == ["test_method_1"]

    def test_method_2(self):
        """Check the contents of ``self.executed``."""
        assert self.executed == ["test_method_1", "test_method_2"]
