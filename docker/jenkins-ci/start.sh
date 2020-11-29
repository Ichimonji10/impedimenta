#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

persistent_dir='/var/jenkins_home'

sudo mkdir --parents "${persistent_dir}"
sudo chown --recursive 1000 "${persistent_dir}"
docker image build --tag jamtur01/jenkins .
docker container run \
    --detach \
    --publish 8080:8080 \
    --publish 50000:50000 \
    --volume "${persistent_dir}:${persistent_dir}" \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --name jenkins jamtur01/jenkins
docker container logs jenkins --follow
xdg-open http://localhost:8080
