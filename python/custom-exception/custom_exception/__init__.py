"""Demonstrate how custom exceptions with ``__str__`` defined behave."""
import io
from pathlib import Path

PATH = Path("/foo/bar.txt")
SEPARATOR: str = "\n" * 3


def main() -> None:
    """Print several custom exceptions, then raise one."""
    print(PATH)
    for err_cls in (CthulhuError, FileAbsentError, FileCorruptError):
        print(SEPARATOR)
        print(type(err_cls))
        print(err_cls(PATH))


class BaseError(Exception):
    """Base class for custom exceptions defined by this package."""


class CthulhuError(BaseError):
    """Cthulhu is present; filesystem issues are the least of your issues.

    The purpose of this class is to provide an exception with no custom
    ``__str__`.
    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path


class FileAbsentError(BaseError):
    """A file is absent from the filesystem.

    The purpose of this class is to provide an exception with a one-line custom
    ``__str__``.
    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path

    def __str__(self) -> str:
        return f"The file at the following path is absent: {self._path}"


class FileCorruptError(BaseError):
    """A file is corrupt.

    The purpose of this class is to provide an exception with a single-line
    custom ``__str__``.
    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self._path = path

    def __str__(self) -> str:
        with io.StringIO() as msg:
            msg.write(f"The file at the following path is corrupt: {self._path}\n")
            msg.write("\n")
            msg.write("Consider the following remediations:\n")
            msg.write("\n")
            msg.write("* Remove the cat from your computer.\n")
            msg.write(
                "* Give a toast to the wayward bits and wish them a merry journey.\n"
            )
            msg.write("* Take a stroll outside.")
            return msg.getvalue()


if __name__ == "__main__":
    main()
