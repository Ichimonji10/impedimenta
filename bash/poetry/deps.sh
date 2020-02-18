#!/usr/bin/env bash
# coding=utf-8
#
# Demonstrate how poetry handles dependency resolution logic.
#
# Poetry correctly resolves dependencies and downgrades them as necessary.
# However, poetry has a bug which prevents it from correctly building wheels in
# certain cases. See: https://github.com/python-poetry/poetry/issues/1689
#
# poetry must be installed system-wide. This script could be re-written without
# it, but its presence simplifies this script.
set -euo pipefail


# Create a temp dir, and schedule it for deletion.
cleanup() {
    if [ -n "${workspace:-}" ]; then rm -rf "${workspace}"; fi
}
trap cleanup EXIT  # bash pseudo signal
trap 'cleanup ; trap - SIGINT ; kill -s SIGINT $$' SIGINT
trap 'cleanup ; trap - SIGTERM ; kill -s SIGTERM $$' SIGTERM
workspace="$(mktemp --directory)"


# Create several packages, each of which depends on a different version of
# requests.
minor_ver=22
for package in plugin-{a,b,c,d}; do
    echo
    echo "Creating and configuring package '${package}'"
    echo
    cd "${workspace}"
    poetry new "${package}"
    cd "${package}"
    poetry run pip install --upgrade pip
    poetry add "requests<2.${minor_ver}"
    minor_ver="$((minor_ver - 1))"
done


# Create a "core" package, and make it depend upon each of the other packages in
# turn. This should cause poetry to continually downgrade dependencies listed in
# poetry.lock in this package.
echo
echo "Creating and configuring package 'core'"
echo
cd "${workspace}"
poetry new core
cd core
poetry run pip install --upgrade pip
poetry add ../plugin-a
poetry add ../plugin-b
poetry add ../plugin-c  --optional
poetry add ../plugin-d  --optional
cat >>pyproject.toml <<EOF

[tool.poetry.extras]
plugins = ["plugin-c", "plugin-d"]
EOF
poetry update  # let poetry handle changes to pyproject.toml
poetry install --extras plugins


# Show the dependency trees for each package.
for package in plugin-{a,b,c,d} core; do
    cd "${workspace}/${package}"
    echo
    echo "Dependencies for package ${package}:"
    echo
    poetry show
done
