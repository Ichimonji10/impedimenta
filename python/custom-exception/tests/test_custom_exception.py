"""Raise custom exceptions."""
from custom_exception import PATH, FileAbsentError, FileCorruptError, CthulhuError


def test_ct_err():
    """Raise CthulhuError."""
    raise CthulhuError(PATH)


def test_fa_err():
    """Raise FileAbsentError."""
    raise FileAbsentError(PATH)


def test_fc_err():
    """Raise FileCorruptError."""
    raise FileCorruptError(PATH)
