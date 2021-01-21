#!/usr/bin/env bash
# coding=utf-8
#
# Start a swarm service.
set -euo pipefail

docker service create \
    --mode global \
    --name global_heyworld \
    ubuntu /bin/sh -c 'while true; do echo hey world; sleep 1; done'
