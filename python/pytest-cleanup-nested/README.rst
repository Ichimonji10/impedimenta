pytest-cleanup-nested
=====================

Muck around with pytest to see how it handles nested fixtures.

Let's say you write a nested pair of fixtures, where:

#.  One fixture, ``inner``, yields a value, and performs a clean-up action during fixture tear-down.
#.  Another fixture, ``outer``, returns inner.
#.  A test case makes use of ``outer``.

When will the tear-down code in ``inner`` execute? Will the use of ``return`` in ``outer`` cause
immediate execution of tear-down code, or will pytest delay execution of tear-down code until after
the test case returns?

The code in this package indicates that the tear-down code executes after the test case returns.
