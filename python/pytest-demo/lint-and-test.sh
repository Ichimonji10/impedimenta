#!/usr/bin/env bash
# coding=utf-8
#
# Lint source code.
set -euo pipefail


poetry run pylint pytest_demo tests
poetry run mypy .
poetry run pytest
