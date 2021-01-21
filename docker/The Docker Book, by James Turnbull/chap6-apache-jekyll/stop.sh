#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

source common.sh

docker container stop "${repo}_server"
docker container rm "${repo}_server"
docker container rm "${repo}_compiler"
