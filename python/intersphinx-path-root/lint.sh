#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

poetry run pylint docs/conf.py
poetry run black --check .
