#!/usr/bin/env bash
# coding=utf-8
#
# Create `.leader.env`.
set -euo pipefail

cat >.leader.env <<EOF
my_hostname="$(hostnamectl --transient)"
my_ip="$(
    ip -json -family inet addr show enp1s0 \
    | jq --raw-output .[0].addr_info[0].local
)"
EOF
