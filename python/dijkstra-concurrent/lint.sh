#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

pylint main.py
mypy main.py
