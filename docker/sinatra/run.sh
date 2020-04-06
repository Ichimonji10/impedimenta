#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

docker image build --tag ichi/sinatra .
docker container run \
    --detach \
    --publish 4567 \
    --volume "${PWD}/webapp":/opt/webapp:ro \
    ichi/sinatra
