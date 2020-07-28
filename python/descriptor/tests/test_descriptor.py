"""Unit tests for the descriptor module."""
import pytest

from descriptor import Temperature


@pytest.mark.parametrize("in_c,out_c", ((0, 0), (-10, -10), (10, 10)))
def test_get_celsius(in_c, out_c):
    """Get a celsius value from a ``Temperature`` object."""
    temp = Temperature(in_c)
    assert temp.celsius == out_c


@pytest.mark.parametrize("in_c,out_f", ((0, 32), (-10, 14), (10, 50)))
def test_get_fahrenheit(in_c, out_f):
    """Get a fahrenheit value from a ``Temperature`` object."""
    temp = Temperature(in_c)
    assert temp.fahrenheit == out_f


@pytest.mark.parametrize("in_c,out_c,out_f", ((-10, -10, 14), (0, 0, 32), (10, 10, 50)))
def test_set_celsius(in_c, out_c, out_f):
    """Set a celsius value on a ``Temperature`` object."""
    temp = Temperature(0)
    temp.celsius = in_c
    assert temp.celsius == out_c
    assert temp.fahrenheit == out_f


@pytest.mark.parametrize("in_f,out_c,out_f", ((14, -10, 14), (32, 0, 32), (50, 10, 50)))
def test_set_fahrenheit(in_f, out_c, out_f):
    """Set a fahrenheit value on a ``Temperature`` object."""
    temp = Temperature(0)
    temp.fahrenheit = in_f
    assert temp.celsius == out_c
    assert temp.fahrenheit == out_f
