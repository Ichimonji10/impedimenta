#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

docker build -t docs .
docker container run --publish 8080:80 docs
