"""A demonstration of the ``__get__`` and ``__set__`` methods.

In ``__get__`` methods, ``instance`` is an instance, whereas ``owner`` is a class.
"""


class Celsius:
    """A temperature, expressed in degrees celsius.

    Do not directly instantiate instances of this class; it isn't meant to be used by itself.
    Instead, use the ``Temperature`` class.
    """

    def __get__(self, instance: "Temperature", owner: "Temperature") -> float:
        """Get a temperature, in degrees celsius, from a ``Temperature`` object."""
        return instance._baseline

    def __set__(self, instance: "Temperature", value: float) -> None:
        """Set a temperature, in degrees celsius, on a ``Temperature`` object."""
        instance._baseline = value


class Fahrenheit:
    """A temperature, expressed in degrees fahrenheit.

    Do not directly instantiate instances of this class; it isn't meant to be used by itself.
    Instead, use the ``Temperature`` class.
    """

    def __get__(self, instance: "Temperature", owner: "Temperature") -> float:
        """Get a temperature, in degrees fahrenheit, from a ``Temperature`` object."""
        return _c_to_f(instance._baseline)

    def __set__(self, instance: "Temperature", value: float) -> None:
        """Set a temperature, in degrees fahrenheit, on a ``Temperature`` object."""
        instance._baseline = _f_to_c(value)


class Temperature:  # pylint:disable=too-few-public-methods
    """A temperature, expressed in one of several units of measurement."""

    celsius = Celsius()
    fahrenheit = Fahrenheit()

    def __init__(self, celsius: float) -> None:
        """Initialize instance variables."""
        self._baseline = celsius


def _c_to_f(celsius: float) -> float:
    return celsius * 1.8 + 32


def _f_to_c(fahrenheit: float) -> float:
    return (fahrenheit - 32) / 1.8
