#!/usr/bin/env bash
# coding=utf-8
#
# Demonstrate how multiple Python packages may be installed into a single venv
# in editable mode, some by poetry, others by pip and setuptools.
#
# poetry doesn't need to be installed system-wide for this script, as this
# script will install poetry into a venv.
set -euo pipefail


# Create a temp dir, and schedule it for deletion.
cleanup() {
    if [ -n "${workspace:-}" ]; then rm -rf "${workspace}"; fi
}
trap cleanup EXIT  # bash pseudo signal
trap 'cleanup ; trap - SIGINT ; kill -s SIGINT $$' SIGINT
trap 'cleanup ; trap - SIGTERM ; kill -s SIGTERM $$' SIGTERM
workspace="$(mktemp --directory)"


# Create a venv.
cd "${workspace}"
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install poetry


# Create and install a Python package, "foo," with poetry.
poetry new foo
cd foo
cat >>foo/__init__.py <<EOF

FOO_CONST = 'foo const'
EOF
poetry install


# Create and install a Python package, "bar," with pip and setuptools.
cd "${workspace}"
mkdir -p bar/bar
cd bar
cat >setup.py <<EOF
#!/usr/bin/env python3
# coding=utf-8
"""A setuptools-based script for installing bar."""
from setuptools import find_packages, setup

setup(
    name='bar',
    version='0.0.1',
    packages=find_packages(),
)
EOF
cat >bar/__init__.py <<EOF
# coding=utf-8

BAR_CONST = 'bar const'
EOF
pip install -e .


# Demonstrate that both packages are usable.
cd "${workspace}"
res="$(python -c 'from foo import FOO_CONST; print(FOO_CONST)')"
echo "FOO_CONST should have a value of 'foo const'. Its value is: ${res}"
res="$(python -c 'from bar import BAR_CONST; print(BAR_CONST)')"
echo "BAR_CONST should have a value of 'bar const'. Its value is: ${res}"


# Edit both constants.
sed -i 's/foo const/modified foo const/' "foo/foo/__init__.py"
sed -i 's/bar const/modified bar const/' "bar/bar/__init__.py"
res="$(python -c 'from foo import FOO_CONST; print(FOO_CONST)')"
echo "FOO_CONST should have a value of 'foo const'. Its value is: ${res}"
res="$(python -c 'from bar import BAR_CONST; print(BAR_CONST)')"
echo "BAR_CONST should have a value of 'bar const'. Its value is: ${res}"
