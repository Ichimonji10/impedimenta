#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

docker image build --tag ichi/redis redis/
docker image build --tag ichi/sinatra .

docker network create chapter-5

docker container run \
    --detach \
    --name=db \
    --net=chapter-5 \
    --publish=6379 \
    ichi/redis \
    --protected-mode no
docker container run \
    --detach \
    --name=logic \
    --net=chapter-5 \
    --publish=4567 \
    --volume="${PWD}/webapp_redis":/opt/webapp:ro \
    ichi/sinatra
