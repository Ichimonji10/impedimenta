Dep Mismatch
============

The purpose of this Python package is to demonstrate what happens when a package
depends on version X of some dependency, but the system provides version Y of
that dependency.

.. contents::

Usage
-----

The intended use case
scenario is as follows:

#.  Create package with the provided ``PKGBUILD``. (Tested on Arch Linux;
    execute ``makepkg``.)
#.  Install the resultant package.
#.  Execute ``dep-mismatch``.

As of this writing, the Arch Linux repositories provide ``python-dateutil``
version 2.8.1, but this package depends on ``python-dateutil<2.8.1``! If it is
possible for a package to use a version of a dependency other than what is
specified in ``setup.py``, then the executable should successfully print a
message like the following::

    The string "2020-01-21T11:35-05" was parsed as 2020-01-21 11:35:00-05:00

Otherwise, the executable should produce an error like the following::

    pkg_resources.DistributionNotFound: The 'python-dateutil<2.8.1' distribution was not found and is required by dep-mismatch

Discussion
----------

Why is it useful to figure out whether a setuptools package can make use of a
dependency of a version different than what is specified in ``setup.py``? This
is useful because it guides the work of developers and packagers.

It is good practice for a Python package to constrain the versions of all
dependencies. This means that for a setuptools-based package, ``setup.py``
should list abstract dependencies like ``python-dateutil<2.8.1``, and another
file (typically ``requirements.txt``) would list concrete dependencies like
``python-dateutil==2.8.0``.

This poses a problem for Linux distribution package maintainers. When creating a
package, should they also add dependencies, like ``python-dateutil<2.8.1``?
Doing so will prevent the system as a whole from updating ``python-dateutil`` to
a newer version, like 2.8.1. That's great for the specific package which did the
pinning, but terrible for the system as a whole.

However, if the dependencies listed in ``setup.py`` or ``requirements.txt`` are
merely *suggestions*, and Python ultimately resolves imports at runtime with
whatever happens to be installed on the system, then this conflict is a
non-issue. Python package developers are free to set dependencies on whichever
package versions they wish, and package maintainers are free to ignore those
version constraints when doing so is best for the system as a whole.

Separately, it's worth noting that `python-dateutil`_ is outdated when parsing
ISO 8601 strings, as Python 3.7 adds `datetime.datetime.fromisoformat`_.
However, it serves as a nice demonstration dependency because it's still widely
available, and it works entirely offline (unlike e.g. requests).

Results
-------

The author has found that when the ``dep-mismatch-git`` package is built and
installed, and ``dep-mismatch`` is executed, then an error is raised. The script
does not successfully execute. This means that the version constraints listed in
``setup.py`` are checked at runtime.

.. _datetime.datetime.fromisoformat: https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat
.. _python-dateutil: https://pypi.org/project/python-dateutil/
