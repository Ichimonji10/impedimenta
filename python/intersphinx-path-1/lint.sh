#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

poetry run pylint intersphinx_path_1 docs/conf.py
poetry run python -m unittest discover tests
poetry run black --check .
