#!/usr/bin/env bash
# coding=utf-8
#
# Demonstrate how multiple Python projects may be installed in editable mode by
# poetry. poetry doesn't need to be installed system-wide for this script, as
# this script will install poetry into a venv.
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


# Create a Python package, "child," and demonstrate that poetry installs
# packages in editable mode by default.
poetry new child
cd child
poetry install
cat >>child/__init__.py <<EOF

CHILD_CONST = 'child const'
EOF
cd /
res="$(python -c 'from child import CHILD_CONST; print(CHILD_CONST)')"
echo "CHILD_CONST should have a value of 'child const'. Its value is: ${res}"
[[ $res == 'child const' ]]


# Create a second Python package, "parent," and demonstrate that it can access
# values in the child package.
cd "${workspace}"
poetry new parent
cd parent
poetry install
cat >>parent/__init__.py <<EOF

from child import CHILD_CONST
PARENT_CONST = CHILD_CONST
EOF
cd /
res="$(python -c 'from parent import PARENT_CONST; print(PARENT_CONST)')"
echo "PARENT_CONST should have a value of 'child const'. Its value is: ${res}"
[[ $res == 'child const' ]]


# Demonstrate that the parent package can see changes in the child package.
sed -i 's/child const/modified child const/' \
    "${workspace}/child/child/__init__.py"
res="$(python -c 'from parent import PARENT_CONST; print(PARENT_CONST)')"
echo "PARENT_CONST should have a value of 'modified child const'. Its value is: ${res}"
[[ $res == 'modified child const' ]]
