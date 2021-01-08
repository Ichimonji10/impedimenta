#!/usr/bin/env bash
# coding=utf-8
#
# Start the swarm leader.
set -euo pipefail

my_ip="$(
    ip -json -family inet addr show enp1s0 \
    | jq --raw-output .[0].addr_info[0].local
)"
docker swarm init --advertise-addr "${my_ip}"
