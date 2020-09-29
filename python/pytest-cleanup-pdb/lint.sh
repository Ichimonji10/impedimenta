#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

poetry run pre-commit install-hooks
poetry run pre-commit run --files $(git ls-files)
