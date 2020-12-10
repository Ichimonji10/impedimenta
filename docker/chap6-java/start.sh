#!/usr/bin/env bash
# coding=utf-8
#
# For information on `docker inspect`:
#
# * https://golang.org/pkg/text/template/
# * https://docs.docker.com/engine/reference/commandline/inspect/#find-a-specific-port-mapping
set -euo pipefail

docker image build --tag jamtur01/fetcher fetcher
docker container run --name fetcher jamtur01/fetcher \
    https://tomcat.apache.org/tomcat-7.0-doc/appdev/sample/sample.war

docker image build --tag jamtur01/server server
docker container run --name server --volumes-from fetcher --publish-all --detach jamtur01/server
host_ip_port="$(docker inspect server \
    --format '{{ index . "NetworkSettings" "Ports" "8080/tcp" 0 "HostIp" }}:{{ index . "NetworkSettings" "Ports" "8080/tcp" 0 "HostPort" }}')"
xdg-open "http://${host_ip_port}/sample"
