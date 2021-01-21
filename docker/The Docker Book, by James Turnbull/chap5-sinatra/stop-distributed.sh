#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

docker container stop db logic
docker container rm db logic
docker network rm chapter-5
