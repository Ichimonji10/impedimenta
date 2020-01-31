#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

poetry run black .
poetry run pylint custom_exception
poetry run mypy .
