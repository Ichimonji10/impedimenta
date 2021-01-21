#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

docker-compose build
docker-compose up
