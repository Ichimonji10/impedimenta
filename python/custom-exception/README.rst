Custom Exception
================

Define several custom exception classes. Provide them all with the same data, but provide differing
defintions of ``__str__`` on each of them:

``CthulhuError``
    Has no custom ``__str__``.

``FileAbsentError``
    Has a single-line ``__str__``.

``FileCorruptError``
    Has a multi-line ``__str__``.

The main file instantiates and prints these exceptions. The unit tests instantiate and raise these
exceptions.

Sample output::

    $ poetry run python custom_exception/__init__.py
    /foo/bar.txt




    <class 'type'>





    <class 'type'>
    The file at the following path is absent: /foo/bar.txt




    <class 'type'>
    The file at the following path is corrupt: /foo/bar.txt

    Consider the following remediations:

    * Remove the cat from your computer.
    * Give a toast to the wayward bits and wish them a merry journey.
    * Take a stroll outside.
    $ poetry run pytest
    ======================================= test session starts ========================================
    platform linux -- Python 3.8.1, pytest-5.3.5, py-1.8.1, pluggy-0.13.1
    rootdir: /home/ichimonji10/code/impedimenta/python/custom-exception
    collected 3 items

    tests/test_custom_exception.py FFF                                                           [100%]

    ============================================= FAILURES =============================================
    ___________________________________________ test_ct_err ____________________________________________

        def test_ct_err():
            """Raise CthulhuError."""
    >       raise CthulhuError(PATH)
    E       custom_exception.CthulhuError

    tests/test_custom_exception.py:7: CthulhuError
    ___________________________________________ test_fa_err ____________________________________________

        def test_fa_err():
            """Raise FileAbsentError."""
    >       raise FileAbsentError(PATH)
    E       custom_exception.FileAbsentError: The file at the following path is absent: /foo/bar.txt

    tests/test_custom_exception.py:12: FileAbsentError
    ___________________________________________ test_fc_err ____________________________________________

        def test_fc_err():
            """Raise FileCorruptError."""
    >       raise FileCorruptError(PATH)
    E       custom_exception.FileCorruptError: The file at the following path is corrupt: /foo/bar.txt
    E
    E       Consider the following remediations:
    E
    E       * Remove the cat from your computer.
    E       * Give a toast to the wayward bits and wish them a merry journey.
    E       * Take a stroll outside.

    tests/test_custom_exception.py:17: FileCorruptError
    ======================================== 3 failed in 0.02s =========================================
