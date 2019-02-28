# coding=utf-8
"""Utilities for functional tests."""
import contextlib
import os
import shutil
import subprocess
import tempfile
from typing import Optional, Sequence


def run(args: Sequence[str]) -> Sequence[str]:
    """Call ``subprocess.run`` with several common arguments set.

    :param args: For details, see the parameter by the same name provided by
        ``subprocess.run``. A command, e.g. ``('echo', 'foo')``.
    :return: The contents of stdout, split on newlines.
    :raise: ``CalledProcessError`` if the called process returns a non-zero
        return code.
    """
    # This annotation is necessary to convince mypy that stdout is a string.
    stdout: str = subprocess.run(
        args,
        check=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        universal_newlines=True,  # convert this OSs newline sequence to \n
    ).stdout
    return stdout.splitlines()


class temp_xdg_data_home(contextlib.ContextDecorator):  # pylint:disable=invalid-name
    """Create a temporary directory and set ``$XDG_DATA_HOME`` to it.

    May be used as either a context manager or a decorator. For example:

    .. code-block:: python

        with temp_xdg_data_home() as temp_xdh:
            temp_file = Path(temp_xdh, 'foo.txt')
            with open(temp_file, 'w') as handle:
                handle.write('foo')

    To learn about ``$XDG_DATA_HOME`` and related concepts, see the `XDG Base
    Directory Specification`_.

    .. WARNING:: If using `PyXDG`_, make sure to `reload`_ the
        ``BaseDirectory`` module before accessing any attributes or executing
        any methods, such as ``BaseDirectory.xdg_data_home``. This is because
        attributes (and the methods, which use them) are set at import time,
        and they ignore modifications that this method makes to the
        environment.

    .. NOTE:: "import" doesn't mean "load", it means "load if not loaded yet
        and then import into namespace". (`Kos`_)

    .. _reload: https://docs.python.org/3.6/library/importlib.html#importlib.reload
    .. _Kos: https://stackoverflow.com/q/437589
    .. _PyXDG: https://www.freedesktop.org/wiki/Software/pyxdg/
    .. _XDG Base Directory Specification:
        https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    """

    def __init__(self) -> None:
        """Initialize this object with instance variables."""
        self.old_xdg_data_home: Optional[str] = None
        self.new_xdg_data_home: str = ''

    def __enter__(self) -> str:
        """Create a temporary directory and set ``$XDG_DATA_HOME``.

        Return the temporary ``$XDG_DATA_HOME``.
        """
        self.old_xdg_data_home = os.environ.get('XDG_DATA_HOME')  # None if unset
        self.new_xdg_data_home = tempfile.mkdtemp()
        os.environ['XDG_DATA_HOME'] = self.new_xdg_data_home
        return self.new_xdg_data_home

    def __exit__(self, *exc) -> None:
        """Reset ``$XDG_DATA_DIR`` and delete the temporary directory."""
        if self.old_xdg_data_home is None:
            del os.environ['XDG_DATA_HOME']
        else:
            os.environ['XDG_DATA_HOME'] = self.old_xdg_data_home
        shutil.rmtree(self.new_xdg_data_home)
