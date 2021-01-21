#!/usr/bin/env bash
# coding=utf-8
#
# It's posible to start multiple instances of a service at once, with a command like:
#
#   docker-compose up --scale server=2
#
# In this case, `docker-compose port` returns the address of one of the servers. (Compose will not
# scale a service beyond one container if, for that service, `container_name` is set.) A more
# powerful method of fetching information about containers is to use `docker inspect`. For more
# information on `docker inspect`:
#
# * https://golang.org/pkg/text/template/
# * https://docs.docker.com/engine/reference/commandline/inspect/#find-a-specific-port-mapping
set -euo pipefail

host_ip_port="$(docker-compose port server 8080)"
xdg-open "http://${host_ip_port}/sample"

for container_id in $(docker-compose ps --quiet -- server); do
    host_ip_port="$(docker inspect "${container_id}" \
        --format '{{ index . "NetworkSettings" "Ports" "8080/tcp" 0 "HostIp" }}:{{ index .  "NetworkSettings" "Ports" "8080/tcp" 0 "HostPort" }}')"
    xdg-open "http://${host_ip_port}/sample"
done
