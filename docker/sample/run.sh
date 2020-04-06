#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

docker image build --tag ichi/nginx .
docker container run \
    --detach \
    --publish 80 \
    --volume "${PWD}/website":/var/www/html/website:ro \
    ichi/nginx \
    nginx
