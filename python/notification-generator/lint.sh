#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

pylint notification_generator
mypy notification_generator
