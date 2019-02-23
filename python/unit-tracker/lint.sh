#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

pylint unit_tracker
mypy unit_tracker
